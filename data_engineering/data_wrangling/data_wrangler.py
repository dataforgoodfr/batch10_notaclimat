from data_engineering.utils.dataclasses_utils import RawDataFrames
from data_engineering.utils.utils import encode
import pandas as pd
from pandas import DataFrame


def wrangle_data(raw_dataframes: RawDataFrames, list_groups: list) -> DataFrame:
    df_coeff_director = raw_dataframes.df_coeff_director.drop(columns=["degre final"])
    df_coeff_director = df_coeff_director.set_index(["Value type", "Courbes"])

    df_pos_cursors = raw_dataframes.df_pos_cursors.copy(deep=True).drop(
        columns=["Catégorie du secteur", "Intervalle", "Commentaire", "level"]).rename(
        columns={"Value type - Grandeur utilisée (évolution annuelle CO2)": "unit",
                 "Borne max (évolution annuelle CO2)": "max",
                 "Borne min (évolution annuelle CO2)": "min"})

    df_pos_cursors = df_pos_cursors.set_index(["unit", "Score"])

    df_global_score = raw_dataframes.df_global_score.copy(deep=True).set_index("Global score")

    df_direct_complete_score = raw_dataframes.df_direct_complete_score.copy(deep=True).set_index(
        "Direct or complete score")

    df_direct_commitment = raw_dataframes.df_direct_commitment.copy(deep=True).set_index("Direct or complete score")

    df_companies_data = raw_dataframes.df_companies_data.copy(deep=True)
    df_companies_data['company_id'] = [encode(x) for x in df_companies_data['Group']]
    df_companies_data['brand_logo'] = df_companies_data['company_id'].apply(lambda x: "assets/Pics/" + x + ".png")

    df_companies_competitors = raw_dataframes.df_companies_competitors.copy(deep=True)
    df_companies_competitors.rename(columns={"Groupe": "Group"}, inplace=True)

    df_companies_data = pd.merge(df_companies_data, df_companies_competitors, how="left", on="Group")

    df_companies_data[["global_score_hexa_color_code", "global_score_short_label",
                       "global_score_logo_path"]] = df_companies_data["Global score"].apply(
        lambda x: df_global_score.loc[x])[["Color Hex", "Short label", "Logo path"]]

    # This computes the various percentages depending on the scenarios along with the cursor level
    c1_perc_scenarios = []
    c1_direct_level = []
    c1_reduc_per_year = []
    c1_final_value = []
    for (k, group) in enumerate(list_groups):
        ini_date = df_companies_data.loc[k, "C1 initial date"]
        fin_date = df_companies_data.loc[k, "C1 final date"]

        if ini_date != "n.a." and fin_date != "n.a.":
            diff_year = int(fin_date) - int(ini_date)

            if df_companies_data.loc[k, "C1 reduction"] != "n.a.":
                c1_final_value.append(100.0 + 100 * float(df_companies_data.loc[k, "C1 reduction"].replace(',', '.')))

            # percentage per scenarios
            dim_perc_2 = float(100.0 * diff_year * float(df_coeff_director.loc[df_companies_data.loc[k, "C1 unit"], '2°C'][0].replace(',', '.')))
            dim_perc_18 = float(100.0 * diff_year * float(df_coeff_director.loc[df_companies_data.loc[k, "C1 unit"], '1,8°C'][0].replace(',', '.')))
            dim_perc_15 = float(100.0 * diff_year * float(df_coeff_director.loc[df_companies_data.loc[k, "C1 unit"], '1,5°C'][0].replace(',', '.')))
            c1_perc_scenarios.append([100.0 + dim_perc_2, 100.0 + dim_perc_18, 100.0 + dim_perc_15])

            # compute direct level of the cursor
            reduc_per_year = float(df_companies_data.loc[k, "C1 reduction"].replace(',', '.')) / diff_year
            min_inter = float(
                df_pos_cursors.loc[df_companies_data.loc[k, "C1 unit"], df_companies_data.loc[k, "C1 direct score"]][
                    "min"].replace(',', '.'))
            max_inter = float(
                df_pos_cursors.loc[df_companies_data.loc[k, "C1 unit"].replace(',', '.'), df_companies_data.loc[k, "C1 direct score"]][
                    "max"].replace(',', '.'))
            c1_reduc_per_year.append(100.0 * reduc_per_year)

            # Just to check some 'weird cases'
            if reduc_per_year < min_inter or reduc_per_year > max_inter:
                print("problem with ", df_companies_data.loc[k, "Group"], "; C1 score in DBB : ",
                      df_companies_data.loc[k, "C1 direct score"],
                      "but the annual reduction is: ", 100.0 * reduc_per_year)

            if df_companies_data.loc[k, "C1 direct score"] == 6.0 and reduc_per_year < min_inter:
                c1_direct_level.append(6.99)  # max level cursor (outside of interval)
            elif df_companies_data.loc[k, "C1 direct score"] == 2.0 and reduc_per_year > max_inter:
                c1_direct_level.append(2.0)  # max level cursor (outside of interval)
            else:
                # linear fit in the score interval
                c1_direct_level.append(
                    float(df_companies_data.loc[k, "C1 direct score"]) + (reduc_per_year - max_inter) / (
                            min_inter - max_inter))
        else:
            c1_perc_scenarios.append(["n.a.", "n.a.", "n.a."])
            c1_direct_level.append("n.a.")
            c1_reduc_per_year.append("n.a.")
            c1_final_value.append("n.a.")

    df_companies_data[["C1 2deg final", "C1 1,8deg final", "C1 1,5deg final"]] = c1_perc_scenarios
    df_companies_data["C1 reduc per year"] = c1_reduc_per_year
    df_companies_data["C1 direct level"] = c1_direct_level
    df_companies_data["C1 final value"] = c1_final_value

    # This assumes that there is always a value for direct score and computes the display related variables
    df_companies_data[["direct_score_hexa_color_code", "direct_score_short_label"]] = \
        df_companies_data["C1 direct score"].apply(lambda x: df_direct_complete_score.loc[x])[
            ["Color Hex", "Short label"]]

    # This computes the various percentages depending on the scenarios along with the cursor level
    c2_perc_scenarios = []
    c2_direct_level = []
    c2_reduc_per_year = []
    c2_final_value = []
    for (k, group) in enumerate(list_groups):
        ini_date = df_companies_data.loc[k, "C2 initial date"]
        fin_date = df_companies_data.loc[k, "C2 final date"]

        if ini_date != "n.a." and fin_date != "n.a.":
            diff_year = int(fin_date) - int(ini_date)

            if df_companies_data.loc[k, "C2 reduction"] != "n.a.":
                c2_final_value.append(100.0 + 100.0 * float(df_companies_data.loc[k, "C2 reduction"].replace(',', '.')))

            # percentage per scenarios
            dim_perc_2 = float(100.0 * diff_year * float(df_coeff_director.loc[df_companies_data.loc[k, "C2 unit"], '2°C'][0].replace(',', '.')))
            dim_perc_18 = float(100.0 * diff_year * float(df_coeff_director.loc[df_companies_data.loc[k, "C2 unit"], '1,8°C'][0].replace(',', '.')))
            dim_perc_15 = float(100.0 * diff_year * float(df_coeff_director.loc[df_companies_data.loc[k, "C2 unit"], '1,5°C'][0].replace(',', '.')))
            c2_perc_scenarios.append([100.0 + dim_perc_2, 100.0 + dim_perc_18, 100.0 + dim_perc_15])

            # compute direct level of the cursor
            reduc_per_year = float(df_companies_data.loc[k, "C2 reduction"].replace(',', '.')) / diff_year
            min_inter = float(
                df_pos_cursors.loc[df_companies_data.loc[k, "C2 unit"], df_companies_data.loc[k, "C2 complete score"]][
                    "min"].replace(',', '.'))
            max_inter = float(
                df_pos_cursors.loc[df_companies_data.loc[k, "C2 unit"], df_companies_data.loc[k, "C2 complete score"]][
                    "max"].replace(',', '.'))
            c2_reduc_per_year.append(100.0 * reduc_per_year)

            # Just to check some 'weird cases'
            if reduc_per_year < min_inter or reduc_per_year > max_inter:
                print("problem with ", df_companies_data.loc[k, "Group"], "; C2 score in DBB : ",
                      df_companies_data.loc[k, "C2 complete score"],
                      "but the annual reduction is: ", 100.0 * reduc_per_year)

            if df_companies_data.loc[k, "C2 complete score"] == 6.0 and reduc_per_year < min_inter:
                c2_direct_level.append(6.99)  # max level cursor (outside of interval)
            elif df_companies_data.loc[k, "C2 complete score"] == 2.0 and reduc_per_year > max_inter:
                c2_direct_level.append(2.0)  # max level cursor (outside of interval)
            else:
                # linear fit in the score interval
                c2_direct_level.append(
                    float(df_companies_data.loc[k, "C2 complete score"]) + (reduc_per_year - max_inter) / (
                            min_inter - max_inter))
        else:
            c2_perc_scenarios.append(["n.a.", "n.a.", "n.a."])
            c2_direct_level.append("n.a.")
            c2_reduc_per_year.append("n.a.")
            c2_final_value.append("n.a.")

    df_companies_data[["C2 2deg final", "C2 1,8deg final", "C2 1,5deg final"]] = c2_perc_scenarios
    df_companies_data["C2 reduc per year"] = c2_reduc_per_year
    df_companies_data["C2 complete level"] = c2_direct_level
    df_companies_data["C2 final value"] = c2_final_value

    # This assumes that there is always a value for complete score and computes the display related variables
    df_companies_data[["complete_score_hexa_color_code", "complete_score_short_label"]] = \
        df_companies_data["C2 complete score"].apply(lambda x: df_direct_complete_score.loc[x])[
            ["Color Hex", "Short label"]]

    # This computes the various percentages depending on the scenarios along with the cursor level
    e1_direct_level = []
    e1_reduc_per_year = []
    e1_final_value = []

    for (k, group) in enumerate(list_groups):

        ini_date = df_companies_data.loc[k, "E1 initial date"]
        fin_date = df_companies_data.loc[k, "E1 final date"]

        if ini_date != "n.a." and fin_date != "n.a.":
            diff_year = int(fin_date) - int(ini_date)
            if df_companies_data.loc[k, "E1 reduction"] != "n.a.":
                e1_final_value.append(100.0 - float(df_companies_data.loc[k, "E1 reduction"].replace(',', '.')))

            # compute direct level of the cursor
            reduc_per_year = -float(df_companies_data.loc[k, "E1 reduction"].replace(',', '.')) / diff_year
            min_inter = 100.0 * float(
                df_pos_cursors.loc[df_companies_data.loc[k, "E1 unit"],
                                   df_companies_data.loc[k, "E1 score commitment direct"]]["min"].replace(',', '.'))
            max_inter = 100.0 * float(
                df_pos_cursors.loc[df_companies_data.loc[k, "E1 unit"],
                                   df_companies_data.loc[k, "E1 score commitment direct"]]["max"].replace(',', '.'))
            e1_reduc_per_year.append(100.0 * reduc_per_year)

            # Just to check some 'weird cases'
            if reduc_per_year < min_inter or reduc_per_year > max_inter:
                print("problem with ", df_companies_data.loc[k, "Group"], "; E1 score in DBB : ",
                      df_companies_data.loc[k, "E1 score commitment direct"],
                      "but the annual reduction is: ", reduc_per_year, "; and interval is: ", min_inter, max_inter)

            if df_companies_data.loc[k, "E1 score commitment direct"] == 6.0 and reduc_per_year < min_inter:
                e1_direct_level.append(6.99)  # max level cursor (outside of interval)
            elif df_companies_data.loc[k, "E1 score commitment direct"] == 2.0 and reduc_per_year > max_inter:
                e1_direct_level.append(2.0)  # max level cursor (outside of interval)
            else:
                # linear fit in the score interval
                e1_direct_level.append(float(df_companies_data.loc[k, "E1 score commitment direct"]) +
                                       (reduc_per_year - max_inter) / (min_inter - max_inter))

        else:
            e1_direct_level.append("n.a.")
            e1_reduc_per_year.append("n.a.")
            e1_final_value.append("n.a.")

    df_companies_data["E1 reduc per year"] = e1_reduc_per_year
    df_companies_data["E1 direct level"] = e1_direct_level
    df_companies_data["E1 final value"] = e1_final_value

    # This assumes that there is always a value for direct score and computes the display related variables
    df_companies_data[["direct_ambition_hexa_color_code", "direct_ambition_long_label"]] = \
        df_companies_data["E1 score commitment direct"].apply(lambda x: df_direct_commitment.loc[x])[
            ["Color Hex", "Short label"]]

    # This computes the various percentages depending on the scenarios along with the cursor level
    e2_direct_level = []
    e2_reduc_per_year = []
    e2_final_value = []

    for (k, group) in enumerate(list_groups):

        ini_date = df_companies_data.loc[k, "E2 initial date"]
        fin_date = df_companies_data.loc[k, "E2 final date"]

        if ini_date != "n.a." and fin_date != "n.a.":
            diff_year = int(fin_date) - int(ini_date)
            if df_companies_data.loc[k, "E2 reduction"] != "n.a.":
                e2_final_value.append(100.0 - float(df_companies_data.loc[k, "E2 reduction"].replace(',', '.')))

            # compute direct level of the cursor
            reduc_per_year = -float(df_companies_data.loc[k, "E2 reduction"].replace(',', '.')) / diff_year
            min_inter = 100.0 * float(
                df_pos_cursors.loc[df_companies_data.loc[k, "E2 unit"],
                                   df_companies_data.loc[k, "E2 score commitment"]]["min"].replace(',', '.'))
            max_inter = 100.0 * float(
                df_pos_cursors.loc[df_companies_data.loc[k, "E2 unit"],
                                   df_companies_data.loc[k, "E2 score commitment"]]["max"].replace(',', '.'))
            e2_reduc_per_year.append(100.0 * reduc_per_year)

            # Just to check some 'weird cases'
            if reduc_per_year < min_inter or reduc_per_year > max_inter:
                print("problem with ", df_companies_data.loc[k, "Group"], "; E2 score in DBB : ",
                      df_companies_data.loc[k, "E2 score commitment"],
                      "but the annual reduction is: ", reduc_per_year, "; and interval is: ", min_inter, max_inter)

            if df_companies_data.loc[k, "E2 score commitment"] == 6.0 and reduc_per_year < min_inter:
                e2_direct_level.append(6.99)  # max level cursor (outside of interval)
            elif df_companies_data.loc[k, "E2 score commitment"] == 2.0 and reduc_per_year > max_inter:
                e2_direct_level.append(2.0)  # max level cursor (outside of interval)
            else:
                # linear fit in the score interval
                e2_direct_level.append(float(df_companies_data.loc[k, "E2 score commitment"]) +
                                       (reduc_per_year - max_inter) / (min_inter - max_inter))

        else:
            e2_direct_level.append("n.a.")
            e2_reduc_per_year.append("n.a.")
            e2_final_value.append("n.a.")

    df_companies_data["E2 reduc per year"] = e2_reduc_per_year
    df_companies_data["E2 complete level"] = e2_direct_level
    df_companies_data["E2 final value"] = e2_final_value

    # This assumes that there is always a value for direct score and computes the display related variables
    df_companies_data[["complete_ambition_hexa_color_code", "complete_ambition_long_label"]] = \
        df_companies_data["E2 score commitment"].apply(lambda x: df_direct_commitment.loc[x])[
            ["Color Hex", "Short label"]]

    # First need to change the type to be a string otherwise it creates problems
    df_companies_data[
        ["Cat 1 amount", "Cat 2 amount", "Cat 3 amount", "Cat 4 amount", "Cat 5 amount", "Cat 6 amount"]] = \
        df_companies_data[
            ["Cat 1 amount", "Cat 2 amount", "Cat 3 amount", "Cat 4 amount", "Cat 5 amount", "Cat 6 amount"]].astype(
            str)

    list_cat_names = []
    list_cat_emissions = []
    list_cat_hover = []

    for (k, group) in enumerate(list_groups):
        list_cat_names.append(",".join(list(
            df_companies_data.loc[
                k, ["Cat 1 name", "Cat 2 name", "Cat 3 name", "Cat 4 name", "Cat 5 name", "Cat 6 name"]])))
        list_cat_emissions.append(",".join(list(df_companies_data.loc[
                                                    k, ["Cat 1 amount", "Cat 2 amount", "Cat 3 amount", "Cat 4 amount",
                                                        "Cat 5 amount", "Cat 6 amount"]])))
        list_cat_hover.append(",".join(list(df_companies_data.loc[k, ["Wording interactive 1", "Wording interactive 2",
                                                                      "Wording interactive 3", "Wording interactive 4",
                                                                      "Wording interactive 5",
                                                                      "Wording interactive 6"]])))

    df_companies_data["emissions_category_name"] = list_cat_names
    df_companies_data["emissions_category_amount"] = list_cat_emissions
    df_companies_data["emissions_category_hover"] = list_cat_names

    df_data_viz = df_companies_data.copy(deep=True)
    df_data_viz = df_data_viz.rename(columns={
        "Group": "company_name",
        "Sector": "sector",
        "C1 final value": "c1_final_value",
        "C1 2deg final": "c1_2deg_final",
        "C1 1,8deg final": "c1_1_8deg_final",
        "C1 1,5deg final": "c1_1_5_deg_final",
        "C1 initial date": "C1_initial_date",
        "C1 final date": "C1_final_date",
        "C1 direct level": "direct_level",
        "C2 final value": "c2_final_value",
        "C2 2deg final": "c2_2deg_final",
        "C2 1,8deg final": "c2_1_8deg_final",
        "C2 1,5deg final": "c2_1_5deg_final",
        "C2 initial date": "C2_initial_date",
        "C2 final date": "C2_final_date",
        "C2 complete level": "complete_level",
        "Comment": "comment",
        "Global score": "global_score",
        "C1 direct score": "direct_score",
        "C2 complete score": "complete_score",
        "E1 score commitment direct": "direct_rounding_score_commitments",
        "E1 direct level": "direct_score_commitments",
        "E1 phrase": "direct_commitments_sentence",
        "E2 score commitment": "complete_rounding_score_commitments",
        "E2 complete level": "complete_score_commitments",

        "E2 phrase": "complete_commitments_sentence",
        "Total emissions": "total_emissions",
        "Country code": "country_flag",

        "Revenue (in bn €)": "revenue",
        "Revenue year": "revenue_year",
        "Total emissions year": "total_emissions_year"

    })

    list_names_var_dataviz = ["company_name", "c1_1_5_deg_final", "c1_1_8deg_final", "c1_2deg_final", "C1_final_date",
                              "c1_final_value", "C1_initial_date", "c2_1_5deg_final", "c2_1_8deg_final",
                              "c2_2deg_final",
                              "C2_final_date", "c2_final_value", "complete_score", "global_score",
                              "complete_score_short_label",
                              "C2_initial_date", "complete_score_hexa_color_code", "direct_score",
                              "direct_score_hexa_color_code",
                              "complete_ambition_hexa_color_code", "complete_rounding_score_commitments",
                              "direct_ambition_hexa_color_code", "direct_rounding_score_commitments",
                              "direct_score_commitments",
                              "complete_score_commitments", "comment", "global_score_hexa_color_code",
                              "global_score_short_label",
                              "direct_score_short_label", "global_score_logo_path", "sector",
                              "complete_ambition_long_label",
                              "complete_commitments_sentence", "direct_ambition_long_label",
                              "direct_commitments_sentence",
                              "emissions_category_amount", "emissions_category_hover", "emissions_category_name",
                              "total_emissions",
                              "total_emissions_year", "brand_logo", "company_id", "country_flag", "revenue",
                              "revenue_year",
                              "direct_level", "complete_level"]

    df_data_viz = df_data_viz[list_names_var_dataviz]

    return df_data_viz
