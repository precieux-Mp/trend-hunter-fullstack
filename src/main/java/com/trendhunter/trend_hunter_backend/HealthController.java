package com.trendhunter.trend_hunter_backend;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController // cette annotation dit: « cette classe gère des requêtes HTTP et renvoie du JSON ».

public class HealthController {
    @GetMapping("/api/health") // Associe cette méthode aux requêtes HTTP GET sur /api/health

    // TODO: Ajoute l'annotation pour dire à Spring de déclencher cette méthode sur un GET vers "/api/health"
    public StatutSante checkHealth() {
        return new StatutSante();
    }
}