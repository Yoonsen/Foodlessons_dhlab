import streamlit as st
import dhlab_v2 as d2
import pandas as pd
from PIL import Image
import urllib


@st.cache(suppress_st_warning=True, show_spinner = False)
def konk(corpus = None, query = None): 
    conc = d2.concordance(urns = list(corpus.index), words = query, limit = 10000)
    try:
        conc['link'] = conc['urn'].apply(
            lambda c: f"""[{str(corpus.loc[c].title) + "-" + str(corpus.loc[c].authors)}]
            (https://www.nb.no/items/{c}?searchText={urllib.parse.quote(query)})"""
        )
    except:
        conc['link'] = conc['urn'].apply(
            lambda c: f"[{c.split('_')[-1]}](https://www.nb.no/items/{c}?searchText={urllib.parse.quote(query)})"
        )
    return conc[['link','conc']]

@st.cache(suppress_st_warning=True, show_spinner = False)
def korpus():
    corpus =  pd.read_csv('corpus.csv', index_col = 0)
    corpus = corpus.set_index('urn')
    return corpus

foodlessons_corpus = korpus()


image = Image.open('NB-logo-no-eng-svart.png')
st.image(image, width = 200)
st.markdown('Se mer om DH ved Nasjonalbiblioteket på [DHLAB-siden](https://nbviewer.jupyter.org/github/DH-LAB-NB/DHLAB/blob/master/DHLAB_ved_Nasjonalbiblioteket.ipynb), og korpusanalyse via web [her](https://beta.nb.no/korpus/)')


st.title('Søk i korpus for *Foodlessons*')

words = st.text_input('Søk etter ord og fraser', "NEAR(østers hummer, 10)")


#st.write(subject_ft, ddk_ft, doctype, period_slider, " ".join(allword))


conc = konk(corpus = foodlessons_corpus, query = words)
st.write("antall treff:", len(conc))
samplesize = st.number_input("Maks antall konkordanser:", 10)

st.markdown(f"## Konkordanser for __{words}__")

st.markdown('\n\n'.join(
    [
        f"{r[1][0]}  {r[1][1]}" 
        for r in 
        conc.sample(
            min(samplesize, len(conc))).iterrows()
    ]
).replace('<b>','**').replace('</b>', '**')
        )


