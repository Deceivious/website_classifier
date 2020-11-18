import pandas as pd

input_file = r"C:\Users\Bigya\Downloads\domain data novelle.xlsx"
df = pd.read_excel(input_file)

df["website_score"] = 0
df.loc[df["status_code"].astype(str) == "200", "website_score"] = df["website_score"] + 200
df.loc[df["status_code"].astype(str) == "300", "website_score"] = df["website_score"] + 50

df.loc[df["robot_classification"].astype(str) == "Multiple inner sitemaps in sitmeap",
       "website_score"] = df["website_score"] + 200
df.loc[df["robot_classification"].astype(str) == "Multiple Pages in sitemap",
       "website_score"] = df["website_score"] + 200
df.loc[df["robot_classification"].astype(str) == "Sitemap found in robots",
       "website_score"] = df["website_score"] + 100
df.loc[df["robot_classification"].astype(str) == "Robots found but no sitemap",
       "website_score"] = df["website_score"] + 50

df["tracker_exists"] = df["tracker_exists"].fillna(False)
df.loc[df["tracker_exists"], "website_score"] = df["website_score"] + 50

df["font_included"] = df["font_included"].fillna(False)
df.loc[df["font_included"], "website_score"] = df["website_score"] + 50

df["auto_scroll"] = df["auto_scroll"].fillna(False)
df.loc[df["auto_scroll"], "website_score"] = df["website_score"] + 50

df["third_party_js"] = df["third_party_js"].fillna(False)
df.loc[df["third_party_js"], "website_score"] = df["website_score"] + 25

df["third_party_platform"] = df["third_party_platform"].fillna(False)
df.loc[df["third_party_platform"], "website_score"] = df["website_score"] + 50

df["has_good_title"] = df["has_good_title"].fillna(False)
df.loc[df["has_good_title"], "website_score"] = df["website_score"] + 50

df["tag_count"] = df["tag_count"].fillna(0)
df.loc[df["tag_count"].between(51, 100, True), "website_score"] = df["website_score"] + 100
df.loc[df["tag_count"].between(101, 200, True), "website_score"] = df["website_score"] + 200
df.loc[201 <= df["tag_count"], "website_score"] = df["website_score"] + 250

df["h1_count"] = df["h1_count"].fillna(0)
df.loc[df["h1_count"] > 0, "website_score"] = df["website_score"] + 50

df["h2_count"] = df["h2_count"].fillna(0)
df.loc[df["h2_count"] > 0, "website_score"] = df["website_score"] + 25
df.loc[df["h2_count"] > 1, "website_score"] = df["website_score"] + 25
df.loc[df["h2_count"] > 4, "website_score"] = df["website_score"] + 25

df["h3_count"] = df["h3_count"].fillna(0)
df.loc[df["h3_count"] > 0, "website_score"] = df["website_score"] + 25
df.loc[df["h3_count"] > 1, "website_score"] = df["website_score"] + 25
df.loc[df["h3_count"] > 4, "website_score"] = df["website_score"] + 25

df["image_count"] = df["image_count"].fillna(0)
df.loc[df["image_count"] < 2, "website_score"] = df["website_score"] - 10
df.loc[df["image_count"] > 1, "website_score"] = df["website_score"] + 25
df.loc[df["image_count"] > 5, "website_score"] = df["website_score"] + 25
df.loc[df["image_count"] > 11, "website_score"] = df["website_score"] + 25

df["logo_count"] = df["logo_count"].fillna(0)
df.loc[df["logo_count"] > 1, "website_score"] = df["website_score"] + 20

df["link_count"] = df["link_count"].fillna(0)
df.loc[df["link_count"] > 0, "website_score"] = df["website_score"] + 10
df.loc[df["link_count"] >= 4, "website_score"] = df["website_score"] + 20
df.loc[df["link_count"] >= 11, "website_score"] = df["website_score"] + 20
df.loc[df["link_count"] >= 21, "website_score"] = df["website_score"] + 10

df["meta_og"] = df["meta_og"].fillna(0)
df.loc[df["meta_og"] > 0, "website_score"] = df["website_score"] + 50

df["meta_facebook"] = df["meta_facebook"].fillna(0)
df.loc[df["meta_facebook"] > 0, "website_score"] = df["website_score"] + 200
df.to_csv(r"D:\computed.tsv", sep="\t", index=False)
