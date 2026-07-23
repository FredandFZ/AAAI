import random 
import pandas as pd

behavior_path = "behaviors-5K.tsv"
impressions_path = "impressions-5K.tsv"
meta_path = "freelancer_meta.tsv" # item meta data

behavior_df = pd.read_csv(behavior_path, sep="\t")
impressions_df = pd.read_csv(impressions_path, sep="\t")
meta_df = pd.read_csv(meta_path, sep="\t")

behavior_demo = behavior_df.sample(n=10)
impressions_demo = impressions_df.sample(n=10)
meta_demo = meta_df.sample(n=3)

behavior_demo.to_csv("behaviors-demo.tsv", sep="\t", index=False)
impressions_demo.to_csv("impressions-demo.tsv", sep="\t", index=False)
meta_demo.to_csv("freelancer_meta-demo.tsv", sep="\t", index=False)