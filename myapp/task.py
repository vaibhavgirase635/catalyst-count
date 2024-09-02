import pandas as pd
from celery import shared_task
from .models import Company
from django.contrib.auth.models import User
import os
from django.conf import settings

@shared_task(serializer='json')
def process_csv_file(file_path,id):
    
    print("file in task..", file_path)
    
    df = pd.read_csv(file_path)
    print(df)
    
    df['name'] = df['name'].fillna(value='Unknown')
    df['domain'] = df['domain'].fillna(value='Unknown')
    df['year founded'] = df['year founded'].ffill()
    df['industry'] = df['industry'].fillna(value='Unknown')
    df['size_range'] = df['size_range'].ffill()
    df['locality'] = df['locality'].fillna(value='Unknown')
    df['country'] = df['country'].fillna(value='Unknown')
    df['linkedin url'] = df['linkedin url'].fillna(value='Unknown')
    df['current employee estimate'] = df['current employee estimate'].ffill()
    df['total employee estimate'] = df['total employee estimate'].ffill()
    user = User.objects.get(id=id)
    for _, row in df.iterrows():
        obj = Company(user=user)
        print(row)
        obj.name = row['name']
        obj.domain = row['domain']
        obj.year_founded = row['year founded']
        obj.industry = row['industry']
        obj.size_range = row['size_range']
        obj.locality = row['locality']
        obj.country = row['country']
        obj.linkedin_url = row['linkedin url']
        obj.current_employee_estimate = row['current employee estimate']
        obj.total_employee_estimate = row['total employee estimate']
        obj.save()
    os.remove(file_path)
    return {"status": True}
