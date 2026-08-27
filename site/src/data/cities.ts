import type { CityDetail } from "@/types/city";
import { sehirSlug } from "@/lib/slug";

const u = (id: string, w = 1400) =>
  `https://images.unsplash.com/${id}?auto=format&fit=crop&w=${w}&q=80`;

const KAPAK = {
  karadeniz: u("photo-1507525428034-b723cf961d3e"),
  yayla: u("photo-1469474968028-56623f02e42e"),
  istanbul: u("photo-1524231757912-21f4fe3a7200"),
  ege: u("photo-1533105079780-92b9be482077"),
  akdeniz: u("photo-1596394516093-50136726872a"),
  kapadokya: u("photo-1570939274717-7eda259b50ed"),
  ic: u("photo-1480714378408-00b8d1e8e1c0"),
  dag: u("photo-1464822759023-fed622ff2c3b"),
  gol: u("photo-1439066615861-d1af74d74000"),
  gap: u("photo-1552832230-c0197dd311b5"),
  orman: u("photo-1441974231531-c6227db76b6e"),
};

const KAPAK_BOLGE: Record<string, string> = {
  "Marmara": KAPAK.istanbul,
  "Ege": KAPAK.ege,
  "Akdeniz": KAPAK.akdeniz,
  "İç Anadolu": KAPAK.ic,
  "Batı Karadeniz": KAPAK.orman,
  "Orta Karadeniz": KAPAK.karadeniz,
  "Doğu Karadeniz": KAPAK.yayla,
  "Doğu Anadolu": KAPAK.dag,
  "Güneydoğu Anadolu": KAPAK.gap,
};

type Satir = [name: string, region: string, summary: string, highlights: string[]];

const SATIRLAR: Satir[] = [
  ["Adana", "Akdeniz", "Seyhan’ın iki yakasında sıcak bir ova kenti. Kebap, taşlık çarşı ve Çukurova’nın bereketi aynı ritimde.", ["Gastronomi", "Ova", "Tarih"]],
  ["Adıyaman", "Güneydoğu Anadolu", "Nemrut’un dev heykelleri gün doğumunda başka bir ölçek kazanır. Kommagene izi, sakin bir Güneydoğu durağı.", ["Tarih", "Doğa", "Arkeoloji"]],
  ["Afyonkarahisar", "Ege", "Termal buhar, kaymak ve kalesi ile İç Ege’nin dinlenme kapısı. Frig vadilerine kısa sapmalar mümkün.", ["Termal", "Gastronomi", "Tarih"]],
  ["Ağrı", "Doğu Anadolu", "Ağrı Dağı ufku ve Doğubayazıt’taki İshak Paşa, yüksek platonun iki simgesi. Yaz kısa, manzara uzun.", ["Dağ", "Tarih", "Doğa"]],
  ["Amasya", "Orta Karadeniz", "Yeşilırmak kıyısında yalıboyu evler ve kral kaya mezarları. Şehzadeler şehri, dar ve photogenic bir vadi.", ["Tarih", "Mimari", "Irmak"]],
  ["Ankara", "İç Anadolu", "Cumhuriyetin idari kalbi; Anıtkabir, müzeler ve bozkırın sade ufku. Gezi ritmi resmi ve net.", ["Tarih & Cumhuriyet", "Müzeler", "Kent"]],
  ["Antalya", "Akdeniz", "Kaleiçi, falez ve Toros etekleri aynı günde birleşir. Akdeniz’in en işlek tatil kapısı.", ["Sahil", "Tarih", "Doğa"]],
  ["Artvin", "Doğu Karadeniz", "Kaçkar etekleri, dar vadiler ve yağmur ormanı hissi. Çoruh kıvrımları yavaş gezilir.", ["Doğa & Yayla", "Trekking", "Nehir"]],
  ["Aydın", "Ege", "İncir, zeytin ve Afrodisias’ın mermer sessizliği. Menderes ovası sakin bir Ege ritmi sunar.", ["Tarih", "Gastronomi", "Ova"]],
  ["Balıkesir", "Marmara", "Kaz Dağları, Ayvalık ve Manyas kuşu; Marmara ile Ege arasında çift kıyı. Zeytinyağı ortak dil.", ["Sahil", "Doğa", "Gastronomi"]],
  ["Bilecik", "Marmara", "Osmanlı’nın ilk izlerini taşıyan küçük bir geçiş ili. Söğüt ve Bozüyük kısa, sakin duraklar.", ["Tarih", "Osmanlı", "Geçiş"]],
  ["Bingöl", "Doğu Anadolu", "Yayla, göl ve termal su; Doğu’nun daha ıslak yüzü. Yaz serinliği için kısa bir kaçış.", ["Yayla", "Termal", "Doğa"]],
  ["Bitlis", "Doğu Anadolu", "Ahlat mezar taşları ve Tatvan’dan Van Gölü bakışı. Taş, rüzgâr ve yüksek plato.", ["Tarih", "Göl", "Mimari"]],
  ["Bolu", "Batı Karadeniz", "Abant, Yedigöller ve Gölcük; İstanbul–Ankara yolunun orman molası. Sis ve çam kokusu.", ["Doğa", "Göller", "Yayla"]],
  ["Burdur", "Akdeniz", "Salda’nın berrak sığlığı ve Sagalassos’un terasları. Göller yöresinin sakin ucu.", ["Göl", "Antik Kent", "Doğa"]],
  ["Bursa", "Marmara", "Osmanlı’nın ilk başkenti; Uludağ, İskender ve hanlar. Yeşil ve çarşı aynı nefeste.", ["Tarih & Osmanlı", "Dağ", "Gastronomi"]],
  ["Çanakkale", "Marmara", "Çanakkale Boğazı, Troya ve Gelibolu. Deniz ve hafıza iç içe.", ["Tarih & Kurtuluş", "Boğaz", "Arkeoloji"]],
  ["Çankırı", "İç Anadolu", "Tuz mağarası ve bozkır kasabası ritmi. Ankara’ya yakın, kalabalıktan uzak.", ["Jeoloji", "Bozkır", "Sakin"]],
  ["Çorum", "Orta Karadeniz", "Hitit başkenti Hattuşa’nın kapısındaki ova kenti. Leblebi ve arkeoloji yan yana.", ["Tarih", "Arkeoloji", "Ova"]],
  ["Denizli", "Ege", "Pamukkale’nin travertenleri ve Hierapolis. Ege’nin iç kesiminde beyaz bir sahne.", ["Doğa", "Antik Kent", "Termal"]],
  ["Diyarbakır", "Güneydoğu Anadolu", "Sur, Hevsel Bahçeleri ve Dicle kıyısı. Taşın ve nehrin kurduğu kadim bir kent.", ["Tarih", "Mimari", "Gastronomi"]],
  ["Edirne", "Marmara", "Selimiye’nin kubbesi Meriç ovasına bakır. Trakya’nın zarif sınır kenti.", ["Mimari", "Tarih", "Nehir"]],
  ["Elazığ", "Doğu Anadolu", "Harput kayalığı ve Keban kıyısı. Doğu’ya açılan sakin bir eşik.", ["Tarih", "Göl", "Kültür"]],
  ["Erzincan", "Doğu Anadolu", "Fırat vadisi, tulum peyniri ve sade bir dağ kenti. Kış net, yaz serin.", ["Doğa", "Gastronomi", "Vadi"]],
  ["Erzurum", "Doğu Anadolu", "Palandöken, Çifte Minare ve yüksek ova. Kış sporunun ve taş medresenin ili.", ["Kış", "Tarih", "Yayla"]],
  ["Eskişehir", "İç Anadolu", "Porsuk kenarı, Odunpazarı evleri ve öğrenci enerjisi. İç Anadolu’nun en yürünebilir kenti.", ["Kent", "Mimari", "Nehir"]],
  ["Gaziantep", "Güneydoğu Anadolu", "Mutfak başkenti; baklava, kebap, mozaik müze. Güneydoğu’nun en canlı sofrası.", ["Gastronomi", "Tarih", "Müze"]],
  ["Giresun", "Doğu Karadeniz", "Fındık bahçeleri ve Ada’ya bakan kıyı. Karadeniz’in daha sakin yeşil duruşu.", ["Sahil", "Doğa", "Yayla"]],
  ["Gümüşhane", "Doğu Karadeniz", "Karaca Mağarası ve dar vadiler. Trabzon–Erzurum arasında serin bir geçit.", ["Mağara", "Doğa", "Vadi"]],
  ["Hakkâri", "Doğu Anadolu", "Cilo–Sat zirveleri ve yüksek sınır vadileri. Yaz kısa, peyzaj keskin.", ["Dağ", "Trekking", "Yayla"]],
  ["Hatay", "Akdeniz", "Antakya mozaiği, asi mutfağı ve mozaik bir kültür. Akdeniz’in en katmanlı kenti.", ["Gastronomi", "Tarih", "Kültür"]],
  ["Isparta", "Akdeniz", "Gül, Eğirdir Gölü ve Davraz. Göller yöresinin kokulu başkenti.", ["Göl", "Doğa", "Gül"]],
  ["Mersin", "Akdeniz", "Kızkalesi, narenciye ve uzun sahil şeridi. Çukurova’nın denize açılan kapısı.", ["Sahil", "Tarih", "Gastronomi"]],
  ["İstanbul", "Marmara", "İki kıta, bir boğaz; imparatorluk katmanları hâlâ yürünebilir. Türkiye’nin en yoğun keşif sahnesi.", ["Tarih", "Boğaz", "Kent"]],
  ["İzmir", "Ege", "Kordon, Agora ve yarımada koyları. Ege’nin açık, rüzgârlı kenti.", ["Sahil", "Tarih", "Kent"]],
  ["Kars", "Doğu Anadolu", "Ani harabeleri, kaşar ve Kafkas rüzgârı. Taş ve bozkırın kuzeydoğu ucu.", ["Tarih", "Mimari", "Gastronomi"]],
  ["Kastamonu", "Batı Karadeniz", "Ilgaz ormanları, çarşı ve etliekmek. Batı Karadeniz’in içe dönük yüzü.", ["Doğa", "Tarih", "Gastronomi"]],
  ["Kayseri", "İç Anadolu", "Erciyes, kapalı çarşı ve pastırma. Kapadokya’nın doğu eşiğindeki dağ kenti.", ["Dağ", "Gastronomi", "Tarih"]],
  ["Kırklareli", "Marmara", "Istranca ormanları ve şaraplık Trakya. Sessiz bir sınır yeşili.", ["Doğa", "Bağ", "Orman"]],
  ["Kırşehir", "İç Anadolu", "Ahi evreni ve termal; bozkırın küçük durak ili. Kapadokya’ya yakın, kalabalıktan uzak.", ["Tarih", "Termal", "Bozkır"]],
  ["Kocaeli", "Marmara", "İzmit Körfezi, yaylalar ve sanayi kıyısı. İstanbul’un doğusundaki geçiş ve nefes.", ["Körfez", "Yayla", "Kent"]],
  ["Konya", "İç Anadolu", "Mevlana, çatalhöyük izi ve geniş ova. Tasavvufun ve buğdayın başkenti.", ["Tarih & Tasavvuf", "Ova", "Kültür"]],
  ["Kütahya", "Ege", "Çini, Frig vadisi ve İznik’ten ayrı bir seramik dili. İç Ege’nin zanaatkâr ili.", ["Zanaat", "Tarih", "Kültür"]],
  ["Malatya", "Doğu Anadolu", "Kayısı bahçeleri ve Eskimalatya izi. Fırat’a bakan sakin bir ova kenti.", ["Gastronomi", "Ova", "Tarih"]],
  ["Manisa", "Ege", "Spil, mesir ve Sardes. İzmir’in ardındaki tarihî ve yeşil eşik.", ["Tarih", "Doğa", "Gastronomi"]],
  ["Kahramanmaraş", "Akdeniz", "Dondurma, kalesi ve Ahır Dağı. Akdeniz ile Güneydoğu arasındaki tok kent.", ["Gastronomi", "Tarih", "Dağ"]],
  ["Mardin", "Güneydoğu Anadolu", "Taş teraslar, Süryani izi ve Mezopotamya ufku. Altın saat burada uzun sürer.", ["Mimari", "Tarih", "Kültür"]],
  ["Muğla", "Ege", "Bodrum, Datça, Fethiye; koy ve palamut. Ege’nin en uzun tatil sahili.", ["Sahil", "Doğa", "Deniz"]],
  ["Muş", "Doğu Anadolu", "Ova, lale mevsimi ve Murat kıyısı. Doğu’nun geniş ve sakin düzlüğü.", ["Ova", "Doğa", "Kültür"]],
  ["Nevşehir", "İç Anadolu", "Peri bacaları, yeraltı şehirleri ve şarap. Kapadokya’nın kalbi.", ["Kapadokya", "Doğa", "Tarih"]],
  ["Niğde", "İç Anadolu", "Aladağlar ve Gümüşler Manastırı. Kapadokya’nın dağlık güney kapısı.", ["Dağ", "Tarih", "Doğa"]],
  ["Ordu", "Orta Karadeniz", "Boztepe, fındık ve Boztepe teleferiği. Samsun–Trabzon arasındaki yeşil kıyı.", ["Sahil", "Yayla", "Doğa"]],
  ["Rize", "Doğu Karadeniz", "Çay bahçeleri, Ayder ve Kaçkar etekleri. En ıslak, en dik Karadeniz.", ["Doğa & Yayla", "Çay", "Trekking"]],
  ["Sakarya", "Marmara", "Sapanca, Acarlar Longozu ve kıyı kumu. İstanbul’a yakın doğa molası.", ["Göl", "Doğa", "Sahil"]],
  ["Samsun", "Orta Karadeniz", "Karadeniz’in incisi; 19 Mayıs ruhu, Kızılırmak ve Yeşilırmak deltaları, Atakum sahili. 17 ilçesi ayrı karakter taşır.", ["Tarih & Kurtuluş", "Doğa & Delta", "Gastronomi"]],
  ["Siirt", "Güneydoğu Anadolu", "Büryan, Boton vadisi ve sade bir taş kent. Güneydoğu’nun daha içe dönük lezzet durağı.", ["Gastronomi", "Vadi", "Kültür"]],
  ["Sinop", "Batı Karadeniz", "En kuzey burun, cezaevi müzesi ve sakin koylar. Karadeniz’in en duru limanlarından.", ["Sahil", "Tarih", "Balık"]],
  ["Sivas", "İç Anadolu", "Medreseler, Kangal ve geniş bozkır. Selçuklu taşının İç Anadolu’daki güçlü durağı.", ["Tarih", "Mimari", "Bozkır"]],
  ["Tekirdağ", "Marmara", "Şarköy bağları, köfte ve Marmara kıyısı. Trakya’nın rakı-meze sahili.", ["Sahil", "Gastronomi", "Bağ"]],
  ["Tokat", "Orta Karadeniz", "Zile, Ballıca Mağarası ve tok at kebabı. Orta Karadeniz’in iç vadi kenti.", ["Tarih", "Gastronomi", "Doğa"]],
  ["Trabzon", "Doğu Karadeniz", "Sümela, Uzungöl ve Boztepe. Doğu Karadeniz’in tarihi ve yayla kapısı.", ["Doğa & Yayla", "Tarih", "Sahil"]],
  ["Tunceli", "Doğu Anadolu", "Munzur vadisi, berrak su ve dağ havası. Doğa ritmi önde, kent küçük.", ["Doğa", "Nehir", "Yayla"]],
  ["Şanlıurfa", "Güneydoğu Anadolu", "Göbeklitepe, Balıklıgöl ve sıra gecesi. İnanç ve arkeolojinin kesiştiği ova.", ["Tarih", "İnanç", "Gastronomi"]],
  ["Uşak", "Ege", "Termal, halı ve Blaundus. İç Ege’nin sakin zanaat ve su durağı.", ["Termal", "Tarih", "Zanaat"]],
  ["Van", "Doğu Anadolu", "Van Gölü, Akdamar ve kahvaltı sofrası. Yüksek platonun en geniş suyu.", ["Göl", "Tarih", "Gastronomi"]],
  ["Yozgat", "İç Anadolu", "Çamlık ve bozkır kasabası sakinliği. Kapadokya–Karadeniz arasında duru bir iç hat.", ["Doğa", "Bozkır", "Sakin"]],
  ["Zonguldak", "Batı Karadeniz", "Maden mirası, falez ve Gökgöl Mağarası. Batı Karadeniz’in endüstriyel kıyısı.", ["Sahil", "Tarih", "Mağara"]],
  ["Aksaray", "İç Anadolu", "Ihlara Vadisi ve Sultanhanı. Kapadokya’nın batı kanyon kapısı.", ["Kanyon", "Tarih", "Doğa"]],
  ["Bayburt", "Doğu Karadeniz", "Çoruh’un yukarı çığırında küçük bir kale kenti. Trabzon–Erzurum arasında sakin durak.", ["Kale", "Doğa", "Vadi"]],
  ["Karaman", "İç Anadolu", "Taşkale, yeşilköy ve Karamanoğlu izi. Konya ovasının güney eşiği.", ["Tarih", "Doğa", "Ova"]],
  ["Kırıkkale", "İç Anadolu", "Kızılırmak kıyısında geçiş kenti. Ankara’ya yakın, kısa bir ırmak durağı.", ["Irmak", "Geçiş", "Kent"]],
  ["Batman", "Güneydoğu Anadolu", "Hasankeyf’in yeni ve eski kıyısı. Dicle vadisinde tarih ve baraj gölü.", ["Tarih", "Vadi", "Göl"]],
  ["Şırnak", "Güneydoğu Anadolu", "Cudi ve Habur eşiği; dağ ile sınırın keskin ili. Yazın kısa, peyzaj tok.", ["Dağ", "Sınır", "Doğa"]],
  ["Bartın", "Batı Karadeniz", "Amasra kalesi ve küçük koylar. Batı Karadeniz’in en photogenic limanı.", ["Sahil", "Tarih", "Kale"]],
  ["Ardahan", "Doğu Anadolu", "Çıldır Gölü, yayla ve Kafkas kapısı. Yazın çiçek, kışın buz.", ["Göl", "Yayla", "Doğa"]],
  ["Iğdır", "Doğu Anadolu", "Ağrı’nın eteklerinde bereketli ova. Kayısı ve sınır düzlüğü.", ["Ova", "Dağ", "Gastronomi"]],
  ["Yalova", "Marmara", "Termal, sahil ve İstanbul’a feribot. Küçük, yeşil bir Marmara molası.", ["Termal", "Sahil", "Doğa"]],
  ["Karabük", "Batı Karadeniz", "Safranbolu’nun Osmanlı sokakları. Ahşap evlerin en derli toplu vitrini.", ["Mimari", "Tarih", "Çarşı"]],
  ["Kilis", "Güneydoğu Anadolu", "Zeytin, künefe ve sınır kasabası sakinliği. Antep mutfağının daha küçük eşiği.", ["Gastronomi", "Sınır", "Kültür"]],
  ["Osmaniye", "Akdeniz", "Karatepe-Aslantaş ve yer fıstığı. Çukurova’nın doğu kapısı.", ["Tarih", "Doğa", "Ova"]],
  ["Düzce", "Batı Karadeniz", "Güzeldere, Efteni ve orman içi göller. Bolu ile kıyı arasında kısa bir yeşil nefes.", ["Şelale", "Göl", "Doğa"]],
];

export const TURKIYE_SEHIRLERI: CityDetail[] = SATIRLAR.map(
  ([name, region, summary, highlights]) => {
    const slug = sehirSlug(name);
    return {
      id: slug,
      name,
      slug,
      region,
      summary,
      coverImage: name === "Nevşehir" ? KAPAK.kapadokya : KAPAK_BOLGE[region] ?? KAPAK.ic,
      highlights,
      available: slug === "samsun",
    };
  },
);

export function sehirDetay(idVeyaSlug: string): CityDetail | undefined {
  return TURKIYE_SEHIRLERI.find((s) => s.id === idVeyaSlug || s.slug === idVeyaSlug);
}
