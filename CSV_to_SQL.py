import pandas as pd
from sqlalchemy import create_engine
from numpy import nan
from sys import argv


def log(message):
    print(f"[INFO] {message}")


log("Loading source data...")

deps = pd.read_csv("./SourceData/populationDepartementsFrance.csv")
histPop = pd.read_csv("./SourceData/populationSerieHistorique2020.csv", sep=";")
metaData = pd.read_csv("./SourceData/populationMetaDataSerieHistorique2020.csv", sep=";")

histPop.fillna(-1, inplace=True)

log("Preparing Regions data...")
Regions = pd.DataFrame()
Regions["codeRegion"] = deps["codeRegion"].unique()
deps_unique = deps.drop_duplicates(subset="codeRegion")
Regions = Regions.merge(deps_unique[['codeRegion', 'nomRegion']], on='codeRegion', how='left')
Regions['codeRegion'] = Regions['codeRegion'].astype(int)

log("Preparing Departements data...")
Departements = pd.DataFrame()
Departements["codeDepart"] = deps["codeDepart"].unique()
deps_unique = deps.drop_duplicates(subset="codeDepart")
Departements = Departements.merge(deps_unique[['codeDepart', 'nomDepart']], on='codeDepart', how='left')
Departements.columns = ["codeDepartement", "nomDepartement"]
Departements["codeRegion"] = deps[deps["codeDepart"] == Departements["codeDepartement"]]["codeRegion"]

log("Preparing Communes data...")
Communes = pd.DataFrame()
Communes[["codeCommune", "nomCommune"]] = metaData[metaData["COD_VAR"] == "CODGEO"][["COD_MOD", "LIB_MOD"]]
Communes["codeDepartement"] = Communes["codeCommune"].apply(lambda val: val[:-2] if val.startswith("97") else val[:-3])
Communes["codeDepartement"] = Communes["codeDepartement"].str.zfill(2)
Communes = Communes.merge(histPop[["CODGEO", "SUPERF"]], how="left", left_on="codeCommune", right_on="CODGEO").drop(columns="CODGEO").rename(columns={"SUPERF": "superficie"})

log("Preparing Annees data...")
Annees = pd.DataFrame(columns=["anneeInf", "anneeSup"])
Annees["anneeInf"] = [1968, 1975, 1982, 1990, 1999, 2009, 2014]
Annees["anneeSup"] = [1975, 1982, 1990, 1999, 2009, 2014, 2020]

histPop.columns = ["CODGEO", "20_POP", "14_POP", "09_POP", "99_POP", "90_POP", "82_POP", "75_POP", "68_POP", "SUPERF",
                   "NAIS1420", "NAIS0914", "NAIS9909", "NAIS9099", "NAIS8290", "NAIS7582", "NAIS6875",
                   "DECE1420", "DECE0914", "DECE9909", "DECE9099", "DECE8290", "DECE7582", "DECE6875", 
                   "20_LOG", "14_LOG", "09_LOG", "99_LOG", "90_LOG", "82_LOG", "75_LOG", "68_LOG"]

log("Preparing Statistiques data...")
statistiques_data = []
for anneeInf, anneeSup in Annees.values:
    log(f"Processing data for period: {anneeInf}-{anneeSup}")
    anneeInf_str = str(anneeInf)[2:]
    anneeSup_str = str(anneeSup)[2:]
    populationDebut_col = f"{anneeInf_str}_POP"
    populationFin_col = f"{anneeSup_str}_POP"
    naissances_col = f"NAIS{anneeInf_str + anneeSup_str}"
    deces_col = f"DECE{anneeInf_str + anneeSup_str}"
    logementsDebut_col = f"{anneeInf_str}_LOG"
    logementsFin_col = f"{anneeSup_str}_LOG"
    filtered_data = histPop[[
        "CODGEO", populationDebut_col, populationFin_col, naissances_col, deces_col,
        logementsDebut_col, logementsFin_col
    ]]
    filtered_data = filtered_data.rename(columns={
        "CODGEO": "codeCommune",
        populationDebut_col: "populationDebut",
        populationFin_col: "populationFin",
        naissances_col: "naissances",
        deces_col: "deces",
        logementsDebut_col: "logementsDebut",
        logementsFin_col: "logementsFin"
    })
    filtered_data["anneeInf"] = anneeInf
    filtered_data["anneeSup"] = anneeSup
    statistiques_data.append(filtered_data)
Statistiques = pd.concat(statistiques_data, ignore_index=True)
Statistiques[Statistiques.columns[1:]] = Statistiques[Statistiques.columns[1:]].astype(int)
Statistiques.columns = [col[0] if isinstance(col, tuple) else col for col in Statistiques.columns]
Statistiques.replace(-1, nan, inplace=True)

def getNvalidate(argv):
    dtb_mapping = {
        "mysql": "mysql+mysqlconnector",
        "postgresql": "postgresql",
        "sqlite": "sqlite",
        "mssql": "mssql+pyodbc"}
    if len(argv) < 4:
        raise ValueError("Insufficient arguments. Expected format: <username> <password> <host> <database_dialect>")
    usr, passw, host, dtb = argv[:4]
    if not usr or not passw or not host or not dtb:
        raise ValueError("None of the arguments can be empty.")
    if dtb not in dtb_mapping:
        raise ValueError(f"Unsupported database DataBase '{dtb}'. Supported DataBases are: {', '.join(dtb_mapping.keys())}")
    return usr, passw, host, dtb_mapping[dtb]

usr, passw, host, dtb = getNvalidate(argv[1:])

log("Creating database engine...")
eng = create_engine(f"{dtb}://{usr}:{passw}@{host}/Statistiques")

log("Writing data into database...")
for table_name, df in [("Regions", Regions), ("Departements", Departements), 
                       ("Communes", Communes), ("Annees", Annees), ("Statistiques", Statistiques)]:
    log(f"Writing table '{table_name}' to the database...")
    df.to_sql(name=table_name, con=eng, if_exists="append", index=False)

log("All data successfully written to the database.")
