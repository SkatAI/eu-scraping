import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import time

def extract_date_from_url(url):
    match = re.search(r'CRE-\d{2}-(\d{4}-\d{2}-\d{2})', url)
    return match.group(1) if match else None


if __name__ == "__main__":

    links = pd.read_csv('./data/extracted_links.csv')
    links.drop_duplicates(inplace = True)
    print(f"We have {links.shape[0]} links")

    BASE_URL = "https://www.europarl.europa.eu"
    output_file = f"./data/debates.json"

    k = 0
    for i, d in links[0:].iterrows():
        k +=1
        current_output_file = f"./data/tmp/debates_{str(k).zfill(4)}.json"
        date = extract_date_from_url(d.url)
        webpage= d.url.split('/')[-1]

        print()
        print(f"{k}/{links.shape[0]}" ,"==", f"{d.url}")

        # Send a GET request to the page
        full_url = BASE_URL + d.url
        response = requests.get(full_url)
        if response.status_code != 200:
            print(f"Failed to load page: {full_url}")

        # Get the page content
        text = BeautifulSoup(response.text, 'html.parser').get_text()
        title = re.search(r"<title>(.*?)</title>", str(response.content)).group(1)


        # split interventions
        parts = [txt.replace('\xa0',' ').replace('–', '-').strip() for txt in  text.split('\xa0\n\xa0\xa0') if len(txt) >5]

        # cases where parts is not a list of interventions
        if len(parts) == 1:
            print(f"-- not a debate")
        else:
            items = []
            part_idx = 0
            for part in parts:
                part_idx +=1
                if "catch the eye" in part.replace('-', ' ').lower():
                    name, party, text  = 'catch the eye', '' , ''
                else:
                    # split the speaker and the text
                    text = '-'.join(part.split(' - ')[1:]).strip()

                    who = part.split(' - ')[0].strip()
                    party = ''
                    match = re.search(r'\((.*?)\)', who)
                    # easiest case, the party right after the speaker name and in parenthesis: john doe (PPE)
                    if match:
                        party = match.group(1)
                        name = who.split('(')[0].strip()

                    # speaker on behalf of party: john doe on behalf of The Left
                    elif len(who.split(',')) >1 :
                        name = who.split(',')[0].strip()
                        # for the time being let's catch everything after the speaker
                        party = who.split(',')[1].strip()

                    else:
                        name = who
                        party = ''

                    if name.lower().strip() == "verbatim report of proceedings":
                        name = ''
                        party = ''
                        text = text.split(' - ')[0].strip()

                    items.append({
                        "parent": d.page,
                        "page_idx" : part_idx,
                        "page": webpage,
                        "title" : title,
                        "name" : name,
                        "party" : party,
                        "text" : text
                    })

            # save
            if len(items) > 1:
                data = pd.DataFrame(items)
                data.to_json(current_output_file, indent= 4, orient = 'records', force_ascii=False)
                print(data.head(2))
                if os.path.exists(output_file):
                    # loa
                    df = pd.read_json(output_file)
                    from_shape = df.shape
                    # concat
                    data = pd.concat([df, data])
                    data.fillna('', inplace = True)
                    data.reset_index(drop = True, inplace = True)
                    # save
                    data.to_json(output_file, indent= 4, orient = 'records', force_ascii=False)
                    # check
                    df = pd.read_json(output_file)
                    print(f"-- from {from_shape} to {df.shape}")
                else:
                    data.to_json(output_file, indent= 4, orient = 'records', force_ascii=False)

        time.sleep(2)




