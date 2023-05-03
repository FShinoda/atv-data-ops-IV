from bs4 import BeautifulSoup
from google.cloud import storage
from google.oauth2 import service_account
import requests
import csv

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

credentials_dict = {
  "type": "service_account",
  "project_id": "cobalt-poet-342917",
  "private_key_id": "8e181146bd5007ca8b021761f4d00d188c7fa435",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCyvJWYMaaZriRg\nv7Niz+wwv6jBRLGAdD1HLGNM8/ht2Y0eDPR3SaEDTVbPpJqRKIAclCXfMFOFy/j0\nRQnn1U4/R1gOzjsvCD37W/Ejag7eq4yz6SwFThAKnonFuPkgpePqHX/Oby+KGirb\nKNdAcQ3ifqBMbxZp2tRy0MUbW6eHyiyFAwykwPp4sI9YWy+MkTZ7Jx2RuRQhTSJZ\nZcaQWL7u99+nUkd1edcwQIln+wqOXUeTzEojbL5N+sLnpD42iNl8aIot77pvzXZp\nHtWJAt9/7aZUcZ8g50WU4AMOcMlP1sL71/4akkBl9ixDe0aWnH5E8Ba1xwX4+zPs\nxVDa6A3bAgMBAAECggEATudgtNjKXtKZHZrTMr5uWtDpSzSrlXT7LkXiqnCTjc75\n9LesXlLDQWVteuoEECvMbpFaLK61WH4Er7Ugm9c3HUk+Dv8s8mTVk/bxO3yRBuy9\nhxjbBZaCD2YQlRhE5oxFUq9mIfhEiNdnbuuXJswh4Iic9FEgGGfx3KPcN+kcyp0P\ni842OzEW/9eaP6LW/NGn3OpPlbp1QYFr9NhiwFmnq0mkqD+NSBspoW65Tyiz/Tct\n+hyErioLtT7C+Q7o5tQqVt/gvd2P2+gMzoKOXIKn1bHasAaAT3/ZoBSRHZahVFUu\ndATGoTb8m9xP33HN2zy1Cts6dJiTadgHPma7pSStSQKBgQD2aDtZ0n88UtGFAfG2\nuTzCaWMTnQVk8YYYJQo8Cax55RfTPJzyX4ubjIRH1z29r7qg0eT5rT1FHdFVye38\n4KcwsUnHS7hqXcaSSjNRHsPcqHMKamf60vqrttKkJrB/D3KWWAjS9CFMnjRrv5q/\nvtFIWVJ72q9YwbhczImPUdyBswKBgQC5se2J64eYb7BYms9dmgskXtWluoycCxKJ\nFcUO99drTerTkhhz7hqjErkl7ZzxyLh4VfBVL2VCkpxASWuJ+HjKPqqMczWIQRD3\ntxj0ksxxOBSj3ryJnOiobr/1P6CxXP+VDf93ei/LJ2DzsUkyfo+Hj3TNQQJTPH7Y\nd5KXGDufOQKBgEpbn/V2KUFJ+MI7mPa8JZLBfM2RZ+xTWlT08Ia3oJ3UPYFYXEBk\nBtw05kJLuO0CF76qOIAEAGZYHjDWVAQowytVhN8ogYlPrTm+PIgxUYfIKZcuDxzJ\nCC5DaINyzXY6cijefiMy2s2lPEp7srZEXiGIGvUXRCzzoLAYZTajzHgzAoGAJefe\nN2Mu4L0b4Fpprg+96oS5VAVKoqfX9sfM3AtXm/3hy6Js/21BXrx5svZYLTrt/RJ9\n5sWwA/DtmGnkW9uuvIoiQl1aNiAiGI71tycoOIxcGj9jeSvgilFhOeztHod/XKvo\n1DjK/MtjDRvJd1dCcUelbiixEtCsi/+Mmu9FbHECgYEAwIldWdgLckqq8SqJc++x\nEZ6+YSdNhMFw1/gqf977/McMRCVTvl1oK2hS0jIbSjoJRPEIttYwysnU3ThYePgH\n4kTEXCvZwwGaX94+aK4vlu9fRclYXj6ACVq0osImmCaR87BahPu9i8U52tWPAhVj\nn+Tpmua083WoKy3VUKuoK1k=\n-----END PRIVATE KEY-----\n",
  "client_email": "gcsaccount@cobalt-poet-342917.iam.gserviceaccount.com",
  "client_id": "107615718522702201070",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/gcsaccount%40cobalt-poet-342917.iam.gserviceaccount.com"
}

try:

  """Uploads a file to the bucket."""
  credentials = service_account.Credentials.from_service_account_info(credentials_dict)
  storage_client = storage.Client(credentials=credentials)
  bucket = storage_client.get_bucket('atv-data-ops-iv') ### Nome do seu bucket
  blob = bucket.blob('artist-names.csv')

  pages = []
  names = "Name \n"

  for i in range(1, 5):
    url = 'https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ' + str(i) + '.htm'
    pages.append(url)

  for item in pages:
    page = requests.get(item)
    soup = BeautifulSoup(page.text, 'html.parser')

    last_links = soup.find(class_='AlphaNav')
    last_links.decompose()

    artist_name_list = soup.find(class_='BodyText')
    artist_name_list_items = artist_name_list.find_all('a')

    for artist_name in artist_name_list_items:
      names = names + artist_name.contents[0] + "\n"

    blob.upload_from_string(names, content_type="text/csv")

except Exception as ex:
  print(ex) 
