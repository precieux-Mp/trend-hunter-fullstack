package com.trendhunter.trend_hunter_backend;



public class StatutSante {

private String nom_application;
private EtatSante etat_sante;
private String version;

// Constructeur

public StatutSante(String nom_application, EtatSante etat_sante, String version){

    this.nom_application = nom_application;
    this.etat_sante = etat_sante;
    this.version = version;

}
//constructeur par défaut
public StatutSante(){
    nom_application = "Trend Hunter API";
    etat_sante= EtatSante.EN_MARCHE;
    version = "1.0.0";
}

// Getters et Setters

public String getNom_application(){
    return nom_application;
}
public EtatSante getEtat_sante(){
    return etat_sante;
}
public String getVersion(){
    return version;
} 
public void setNom_application(String nom_application){
    this.nom_application = nom_application;
}
public void setEtat_sante(EtatSante etat_sante){
    this.etat_sante = etat_sante;
    
}
public void setVersion(String version){
    this.version = version;
}
}