package com.trendhunter.trend_hunter_backend;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import java.util.List;

public interface TendanceRepository extends JpaRepository<Tendance, Long> {

    // Toutes les mesures d'un sujet, de la plus ancienne à la plus récente
    List<Tendance> findBySujetOrderByDateReleveAsc(String sujet);

    // La liste des sujets distincts présents en base
    @Query("SELECT DISTINCT t.sujet FROM Tendance t")
    List<String> trouverSujetsDistincts();
}