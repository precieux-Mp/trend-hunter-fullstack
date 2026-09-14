package com.trendhunter.trend_hunter_backend;
import java.time.LocalDateTime;
import org.hibernate.annotations.CreationTimestamp;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

@Entity
public class Tendance {

    @CreationTimestamp
    private LocalDateTime dateReleve; // horodatage automatique à l'enregistrement

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id; // clé primaire générée automatiquement par la base

    private String sujet;// le mot clé de la tendance
    private double scorePopularite; // le score de popularité de la tendance
    private String source; // la source de la tendance
    private String categorie;// la catégorie de la tendance

    // Constructeur
    public Tendance (String sujet, double scorePopularite, String source, String categorie)  {
        this.sujet = sujet;
        this.scorePopularite = scorePopularite;
        this.source = source;
        this.categorie = categorie;
    }
    //constructeur par défaut
    public Tendance (){
        this.sujet = "Inconnu";
        this.scorePopularite=0.0;
        this.source = "Inconnu";
        this.categorie = "Inconnu";
    }

    // Getters et Setters
    public Long getId(){
        return id;
    }
    public void setId(Long id){
        this.id=id;
    }
    public String getSujet(){
        return sujet;
    }
    public double getScorePopularite (){
        return scorePopularite;
    }
    public String getSource(){
        return source;
    }
    public String getCategorie(){
        return categorie;
    }

    public void setSujet(String s){
        this.sujet=s;
    }
    public void setScorePopularite (double score){
        this.scorePopularite=score;
    }
    public void setSource(String s){
        this.source=s;
    }
    public void setCategorie(String c){
        this.categorie=c;
    }
    public LocalDateTime getDateReleve() {
    return dateReleve;
    }
    public void setDateReleve(LocalDateTime dateReleve) {
        this.dateReleve = dateReleve;
    }

}