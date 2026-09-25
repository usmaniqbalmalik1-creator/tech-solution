import pandas as pd
from pipeline import validate,transform

def test_validation_rejects_bad_rows():
    df=pd.DataFrame([{"customer":"A","category":"X","quantity":2,"revenue":10,"month":"2026-01"},{"customer":"B","category":"X","quantity":0,"revenue":10,"month":"2026-01"}])
    valid,rejected=validate(df)
    assert len(valid)==1 and len(rejected)==1

def test_transform():
    df=pd.DataFrame([{"customer":"A","category":"X","quantity":2,"revenue":10,"month":"2026-01"}])
    out=transform(df)
    assert out.iloc[0]["revenue"]==10
