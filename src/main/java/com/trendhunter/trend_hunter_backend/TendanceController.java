package com.trendhunter.trend_hunter_backend;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import java.util.List;

@CrossOrigin(origins = "*")
@RestController
@RequestMapping("/api/tendances")
public class TendanceController {

    private final TendanceService service;

    public TendanceController(TendanceService service) {
        this.service = service;
    }

    @GetMapping
    public List<Tendance> getTendances() {
        return service.obtenirToutes();
    }

    @PostMapping
    public Tendance addTendance(@RequestBody Tendance tendance) {
        return service.enregistrer(tendance);
    }

    // --- Phase 3 : le top des sujets qui montent ---
    @GetMapping("/emergentes")
    public List<TendanceEmergente> getEmergentes() {
        return service.obtenirEmergentes();
    }
}
