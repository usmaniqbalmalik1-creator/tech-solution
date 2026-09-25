from pathlib import Path
import pandas as pd
from pydantic import BaseModel, ValidationError, Field

class Sale(BaseModel):
    customer:str
    category:str
    quantity:int=Field(gt=0)
    revenue:float=Field(gt=0)
    month:str

def validate(df):
    valid=[]; rejected=[]
    for row in df.to_dict("records"):
        try: valid.append(Sale(**row).model_dump())
        except ValidationError as e: rejected.append({"row":row,"error":str(e)})
    return pd.DataFrame(valid),rejected

def transform(df):
    return (df.groupby(["month","category"],as_index=False)
              .agg(orders=("customer","count"),units=("quantity","sum"),revenue=("revenue","sum"))
              .sort_values(["month","revenue"],ascending=[True,False]))

def main():
    base=Path(__file__).parent
    source=base/"data"/"sales.csv"
    df=pd.read_csv(source)
    valid,rejected=validate(df)
    output=transform(valid)
    output.to_csv(base/"output.csv",index=False)
    pd.DataFrame(rejected).to_json(base/"rejected.json",orient="records",indent=2)
    print(f"Processed {len(valid)} valid rows; rejected {len(rejected)} rows.")

if __name__=="__main__": main()
