package com.trendhunter.trend_hunter_backend;

import org.springframework.stereotype.Service;
import java.util.ArrayList;
import java.util.List;

@Service
public class TendanceService {

    private final TendanceRepository repository;

    public TendanceService(TendanceRepository repository) {
        this.repository = repository;
    }

    public Tendance enregistrer(Tendance tendance) {
        return repository.save(tendance);
    }

    public List<Tendance> obtenirToutes() {
        return repository.findAll();
    }

    // --- Phase 3 : calcul de l'émergence ---
    public List<TendanceEmergente> obtenirEmergentes() {
        List<TendanceEmergente> resultat = new ArrayList<>();

        for (String sujet : repository.trouverSujetsDistincts()) {
            List<Tendance> mesures = repository.findBySujetOrderByDateReleveAsc(sujet);

            if (mesures.size() < 2) continue;          // besoin d'au moins 2 mesures

            Tendance premiere = mesures.get(0);
            Tendance derniere = mesures.get(mesures.size() - 1);

            double scoreInitial = premiere.getScorePopularite();
            double scoreActuel  = derniere.getScorePopularite();

            if (scoreInitial <= 0) continue;           // éviter la division par zéro

            double croissance = ((scoreActuel - scoreInitial) / scoreInitial) * 100.0;

            List<Double> historique = new ArrayList<>();
            for (Tendance m : mesures) historique.add(m.getScorePopularite());

            resultat.add(new TendanceEmergente(
                sujet, derniere.getCategorie(), derniere.getSource(),
                scoreActuel, scoreInitial, croissance, historique
            ));
        }

        // les plus émergents d'abord
        resultat.sort((a, b) -> Double.compare(b.getCroissancePourcent(), a.getCroissancePourcent()));
        return resultat;
    }
}