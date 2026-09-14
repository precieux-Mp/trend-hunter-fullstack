package com.trendhunter.trend_hunter_backend;

import java.util.List;

// Objet de réponse : ce que l'API renvoie pour chaque sujet émergent.
public class TendanceEmergente {

    private String sujet;
    private String categorie;
    private String source;
    private double scoreActuel;
    private double scoreInitial;
    private double croissancePourcent;
    private List<Double> historique;   // pour la mini-courbe (Phase 4)

    public TendanceEmergente(String sujet, String categorie, String source,
                             double scoreActuel, double scoreInitial,
                             double croissancePourcent, List<Double> historique) {
        this.sujet = sujet;
        this.categorie = categorie;
        this.source = source;
        this.scoreActuel = scoreActuel;
        this.scoreInitial = scoreInitial;
        this.croissancePourcent = croissancePourcent;
        this.historique = historique;
    }

    public String getSujet() { return sujet; }
    public String getCategorie() { return categorie; }
    public String getSource() { return source; }
    public double getScoreActuel() { return scoreActuel; }
    public double getScoreInitial() { return scoreInitial; }
    public double getCroissancePourcent() { return croissancePourcent; }
    public List<Double> getHistorique() { return historique; }
}