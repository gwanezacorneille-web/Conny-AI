package com.connyai.v14;

import java.io.IOException;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;

public final class AuthClient {

    private final String baseUrl;

    public AuthClient(String baseUrl) {
        this.baseUrl = baseUrl;
    }

    private String post(String path, String body, String token)
            throws IOException {

        URL url = new URL(
                baseUrl.replaceAll("/$", "") + path
        );

        HttpURLConnection connection =
                (HttpURLConnection) url.openConnection();

        connection.setRequestMethod("POST");
        connection.setRequestProperty(
                "Content-Type",
                "application/json"
        );

        if (token != null && !token.isEmpty()) {
            connection.setRequestProperty(
                    "Authorization",
                    "Bearer " + token
            );
        }

        connection.setDoOutput(true);

        byte[] data =
                body.getBytes(StandardCharsets.UTF_8);

        try (OutputStream output =
                     connection.getOutputStream()) {

            output.write(data);
        }

        int code = connection.getResponseCode();

        if (code < 200 || code >= 300) {
            throw new IOException(
                    "HTTP authentication failed: " + code
            );
        }

        return new String(
                connection.getInputStream().readAllBytes(),
                StandardCharsets.UTF_8
        );
    }

    public String guest() throws IOException {
        return post(
                "/auth/guest",
                "{}",
                null
        );
    }

    public String login(
            String username,
            String password
    ) throws IOException {

        String body =
                "{\"username\":\""
                + escape(username)
                + "\",\"password\":\""
                + escape(password)
                + "\",\"account_type\":\"private\"}";

        return post(
                "/auth/login",
                body,
                null
        );
    }

    public String register(
            String username,
            String password
    ) throws IOException {

        String body =
                "{\"username\":\""
                + escape(username)
                + "\",\"password\":\""
                + escape(password)
                + "\"}";

        return post(
                "/auth/register",
                body,
                null
        );
    }

    public String logout(String token)
            throws IOException {

        return post(
                "/auth/logout",
                "{}",
                token
        );
    }

    private static String escape(String value) {
        return value
                .replace("\\", "\\\\")
                .replace("\"", "\\\"");
    }
}
