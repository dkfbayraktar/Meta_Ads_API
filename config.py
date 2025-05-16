# Ortam değişkenlerinden Meta API Token ve diğer sabit yapılandırmaları okur.

import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# Meta API Token
TOKEN_ID = os.getenv("TOKEN_ID")

# Facebook Graph API base URL ve versiyon
GRAPH_API_BASE = "https://graph.facebook.com"
GRAPH_API_VERSION = "v19.0"

# Tanımlı reklam hesapları sözlüğü (mağaza adı -> {id, name})
AD_ACCOUNTS = {
    "thenichebox": {
        "id": "679253881166774",
        "name": "Dencom_LLC"
    },
    # "store2": {
    #     "id": "123456789012345",
    #     "name": "Another_Store_Name"
    # },
    # "store3": {
    #     "id": "987654321098765",
    #     "name": "Future_Shop_Example"
    # }
}

# NOT: Artık sabit bir DEFAULT_AD_ACCOUNT tanımı kullanılmıyor.
# Çoklu hesap desteği için AD_ACCOUNTS sözlüğü üzerinden döngüyle dinamik kullanım uygulanacaktır.
