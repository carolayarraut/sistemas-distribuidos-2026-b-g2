package co.edu.corhuila.barbersaas.identityauth.app;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.UUID;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.springframework.test.web.servlet.MockMvc;

/**
 * Negative authorization test of story barber-saas-docs #166 (STRIDE E, risk 6, PR #162):
 * only an ADMIN_BARBERSHOP with a barbershopId in the token may call POST /api/v1/auth/barbers.
 */
@SpringBootTest
@AutoConfigureMockMvc
class CreateBarberAuthorizationTest {

    private static final String PASSWORD = "Corte2026";

    @Autowired
    private MockMvc http;

    @DynamicPropertySource
    static void privateKey(DynamicPropertyRegistry registry) {
        InternalHttpTest.privateKey(registry);
    }

    /** Criterion 1: a client cannot give itself a barber account, and no account is created. */
    @Test
    void clientTokenGets403() throws Exception {
        String client = InternalHttpTest.token(UUID.randomUUID().toString(), "CLIENT", null);

        http.perform(createBarber(client, "cp4-client-0001", "fake.barber@example.com"))
                .andExpect(status().isForbidden())
                .andExpect(jsonPath("$.error").value("FORBIDDEN"));

        // identity_auth.app_user got no new row: that e-mail cannot log in.
        http.perform(post("/api/v1/auth/login").contentType(MediaType.APPLICATION_JSON)
                        .content("{\"email\":\"fake.barber@example.com\",\"password\":\"" + PASSWORD + "\"}"))
                .andExpect(status().isUnauthorized());
    }

    /** Criterion 2: the owner role alone is not enough, the token must carry its barbershopId. */
    @Test
    void ownerTokenWithoutBarbershopGets403() throws Exception {
        String ownerWithoutShop = InternalHttpTest.token(UUID.randomUUID().toString(), "ADMIN_BARBERSHOP", null);

        http.perform(createBarber(ownerWithoutShop, "cp4-owner-0002", "no.shop@example.com"))
                .andExpect(status().isForbidden())
                .andExpect(jsonPath("$.error").value("FORBIDDEN"));
    }

    private static org.springframework.test.web.servlet.RequestBuilder createBarber(String token, String key,
                                                                                     String email) {
        return post("/api/v1/auth/barbers")
                .header("Authorization", "Bearer " + token)
                .header("Idempotency-Key", key)
                .contentType(MediaType.APPLICATION_JSON)
                .content("""
                        {"fullName":"Andres Rojas","email":"%s","password":"%s","phone":"+573104445566"}
                        """.formatted(email, PASSWORD));
    }
}
