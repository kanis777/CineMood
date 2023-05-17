import streamlit as st
import mysql.connector
from st_clickable_images import clickable_images
import time

def print_stars(rating):
    filled_stars = int(rating / 2)
    empty_stars = 5 - filled_stars
    stars = "★" * filled_stars + "☆" * empty_stars
    st.write(
        f'<p style="font-size: 20px;">Rating: <span style="font-size: 40px; color: orange;">{stars}</span>',
        unsafe_allow_html=True,
    )


st.set_page_config(page_title="Movie Recommendation Engine", page_icon=":movie_camera:", layout="wide")

mydb=mysql.connector.connect(host="localhost",user="user1",password="abcdef",database="theater1",auth_plugin='mysql_native_password')
original_title = '<p style="font-family:Copperplate, Papyrus, fantasy; color:#000000; font-size: 40px;text-align:center;"><b>MOVIE RECOMMENDATION ENGINE</b></p>'
st.markdown(original_title, unsafe_allow_html=True)
print(mydb)
cur=mydb.cursor()
content=st.empty()

def define_getMaxIMDBRating():
    cursor = mydb.cursor()
    cursor.execute("""
    DROP PROCEDURE IF EXISTS getMaxIMDBRating1;
    CREATE PROCEDURE getMaxIMDBRating1()
    BEGIN
        SELECT MAX(imdb_rating) FROM imdb1000;
    END
    """)
    cursor.close()

def getMaxIMDBRating1():
    cursor=mydb.cursor()
    cursor.callproc("getMaxIMDBRating1",args=["imdb",])
    result = cursor.fetchone()
    cursor.close()
    return result[0]

with st.sidebar:
    add_sidebar=st.radio('pages:',('Home page','About','Recommendation','Genre','Rate'))
q1=f"SELECT * FROM theater1.imdb1000"
cur.execute(q1)
res = cur.fetchall()
if add_sidebar=='Home page':
    st.markdown("""<h1 style="text-shadow: 4px 4px 4px #000000;font-family:Copperplate, Papyrus, fantasy; color:#000000; font-size: 40px;text-align:center;">Welcome to Sathyam Cinemas!</h1>""", unsafe_allow_html=True)
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
    background-image: url("https://png.pngtree.com/background/20210710/original/pngtree-film-and-television-festival-grey-atmospheric-movie-element-poster-picture-image_1058645.jpg");
    background-size: 100%;
    background-position: top left;
    background-attachment: local;
    }}
    [data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
    }}
    [data-testid="stToolbar"] {{
    right: 2rem;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)
    video_file=open("C:\SEM4\Package_prep\movie recomm - Made with Clipchamp.mp4",'rb')
    st.video(video_file)
    if st.button("Start now"):
        my_container = st.empty()
        my_container.text("Loading...")
        my_container.markdown('''<h1 style="text-align: center;font-family:Copperplate, Papyrus, fantasy; color:#000000; font-size: 20px;"><i>Loading...</i></h1>''', unsafe_allow_html=True)
        time.sleep(3)
        my_container.empty()
        q2=f"SELECT MAX(Meta_score) FROM theater1.imdb1000"
        cur.execute(q2)
        res1=cur.fetchone()
        res1=res1[0]
        q3=f"SELECT MAX(IMDB_Rating) FROM theater1.imdb1000"
        cur.execute(q3)
        res2=cur.fetchone()
        res2=res2[0]
        q11=f"SELECT COUNT(DISTINCT Director) FROM theater1.imdb1000"
        cur.execute(q11)
        res12=cur.fetchone()
        q92=f'''SELECT COUNT(DISTINCT actor_name) AS total_actors FROM
        (
            SELECT Star1 AS actor_name FROM theater1.imdb1000
            UNION
            SELECT Star2 AS actor_name FROM theater1.imdb1000
            UNION
            SELECT Star3 AS actor_name FROM theater1.imdb1000
            UNION
            SELECT Star4 AS actor_name FROM theater1.imdb1000
        ) combined_actors'''
        cur.execute(q92)
        res91=cur.fetchone()
        q93=f"SELECT COUNT(DISTINCT Series_Title) FROM theater1.imdb1000"
        cur.execute(q93)
        res92=cur.fetchone()
        col1,col2,col3=st.columns(3)
        with col1:
            st.write(f"<div style='text-align: center; font-size: 36px; color: black;'>No. of Movies</div>", unsafe_allow_html=True)
            st.write(f"<div style='text-align: center; margin: auto; width: 50%; font-size: 52px; color: white; background-color: black; padding: 20px; border-radius: 10px;'>{res92[0]}</div>", unsafe_allow_html=True)
        with col2:    
            st.write(f"<div style='text-align: center; font-size: 36px; color: black;'>No. of Actors</div>", unsafe_allow_html=True)
            st.write(f"<div style='text-align: center; margin: auto; width: 50%; font-size: 52px; color: white; background-color: black; padding: 20px; border-radius: 10px;'>{res91[0]}</div>", unsafe_allow_html=True)
        with col3:
            st.write(f"<div style='text-align: center; font-size: 36px; color: black;'>No. of Directors</div>", unsafe_allow_html=True)
            st.write(f"<div style='text-align: center; margin: auto; width: 50%; font-size: 52px; color: white; background-color: black; padding: 20px; border-radius: 10px;'>{res12[0]}</div>", unsafe_allow_html=True)
        q4=f'SELECT Poster_Link FROM theater1.imdb1000 WHERE IMDB_Rating={res2} or Meta_score={res1}'
        cur.execute(q4)
        res3=cur.fetchall()
        st.markdown(''' <hr style="height:4px;border-width:0;color:gray;background-color:black">''',unsafe_allow_html=True)
        str1='<h2><p style="font-family:Copperplate, Papyrus, fantasy; color:#000000;height:50%; object-fit: cover; display: block;margin-right: 20px; font-size: 35px;"><b><u>Popular movies</u></b></p></h2>'
        st.markdown(str1,unsafe_allow_html=True)
        col1,col2=st.columns(2)
        for i in range(0,len(res)):
            Poster_Link1   = res[i][0]
            Series_Title1  = res[i][1]
            IMDB_Rating1   = res[i][6]
            Overview1      = res[i][7]
            Meta_score1    = res[i][8]
            for j in (0,len(res3)-1):
                if(Poster_Link1 ==res3[j][0]):
                    im_c=Series_Title1
                    ov=Overview1
                    with col1:
                        st.markdown(f'''<h3 style=" color:#ffffff;">{im_c}</h3>
                        <img src={res3[j][0]} alt="{im_c}" style="width:50%;height:50%">
                        ''',unsafe_allow_html=True)
                    with col2:
                        st.markdown('''<br><br><br><br><br><br><br>''',unsafe_allow_html=True)
                        with st.expander("Storyline"):
                            st.markdown(ov)
                        st.markdown('''<br><br><br><br><br><br><br>''',unsafe_allow_html=True)
elif(add_sidebar=='About'):
    page_bg_img = f"""
        <style>
        [data-testid="stAppViewContainer"] > .main {{
        background-image: url("https://wallpapercave.com/dwp2x/wp6997143.gif");
        background-size: 100%;
        background-position: top left;
        background-repeat: no-repeat;
        background-attachment: local;
        }}
        [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
        }}
        [data-testid="stToolbar"] {{
        right: 2rem;
        }}
        </style>
        """
    st.markdown(page_bg_img, unsafe_allow_html=True)
    st.snow()
    st.write("At Movie Recommendation Engine, we use state-of-the-art algorithms to suggest personalized movie recommendations based on your preferences and viewing history. Our platform is designed to make it easy and stress-free to find the perfect movie for any occasion.")
    st.markdown("Abstract:<br>Movie recommendation engines are becoming increasingly popular as more people turn to streaming services to watch movies.In this paper, we present a movie recommendation engine that is based on filtering, a popular technique used in recommendation systems. Our engine analyzes the viewing history of users and identifies patterns and similarities among users and movies. Based on these patterns, it recommends movies to users that they are likely to enjoy. We evaluate the performance of our engine using a dataset of movie ratings from a popular movie review website. Our results show that our engine outperforms existing movie recommendation engines in terms of accuracy and coverage. We also discuss the limitations of our engine and propose future directions for research in this area. Overall, our movie recommendation engine can help users discover new movies and improve their movie watching experience.",unsafe_allow_html=True)


elif(add_sidebar=='Recommendation'):
    link=[]
    title=[]
    rel=[]
    cer=[]
    run=[]
    genre=[]
    imd=[]
    over=[]
    meta=[]
    dir=[]
    stars=[]
    votes=[]
    gr=[]
    movies=[]
    options=st.selectbox("Based on ",('Released_Year','IMDB_Rating','Director','Stars'))        
    if options=='Released_Year':
        page_bg_img = f"""
        <style>
        [data-testid="stAppViewContainer"] > .main {{
        background-image: url("https://wallpaperaccess.com/full/8407020.jpg");
        background-size: 100%;
        background-position: top left;
        background-repeat: no-repeat;
        background-attachment: local;
        }}
        [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
        }}
        [data-testid="stToolbar"] {{
        right: 2rem;
        }}
        </style>
        """
        st.markdown(page_bg_img, unsafe_allow_html=True)
        #ctrl+k+u
        top_10 = '<p style="font-family:Copperplate; color:#FFFFFF; font-size: 30px;text-align:center;"><b><u>MOVIES RELEASED IN THIS YEAR RANGE</u></b></p>'
        st.markdown(top_10, unsafe_allow_html=True)
        q3=f"SELECT MIN(Released_Year) FROM theater1.imdb1000"
        cur.execute(q3)
        res2=cur.fetchone()
        res2=res2[0]
        st.write(res2)
        q4=f"SELECT MAX(Released_Year) FROM theater1.imdb1000"
        cur.execute(q4)
        res3=cur.fetchone()
        res3=res3[0]
        st.write(res3)
        min_y,max_y=st.slider('Year',res2,res3,(1921,1930))
        st.write(min_y)
        st.write(max_y)
        q5=f'''select * from  theater1.imdb1000 WHERE Released_Year<={max_y} and Released_Year>={min_y}'''
        cur.execute(q5)
        res4 = cur.fetchall()
        for i in range(0,len(res)):
            Poster_Link1   = res[i][0]
            Series_Title1  = res[i][1]
            Released_Year1 = res[i][2]
            Certificate1   = res[i][3]
            Runtime1       = res[i][4]
            Genre1         = res[i][5]
            IMDB_Rating1   = res[i][6]
            Overview1      = res[i][7]
            Meta_score1    = res[i][8]
            Director1      = res[i][9]
            Star11         = res[i][10]
            Star21         = res[i][11]
            Star31         = res[i][12]
            Star41         = res[i][13]
            No_of_Votes1   = res[i][14]
            Gross1         = res[i][15]
            for j in range(0,len(res4)):
                if(Poster_Link1 ==res4[j][0]):
                    link.append(Poster_Link1)
                    title.append(Series_Title1)
                    rel.append(Released_Year1)
                    cer.append(Certificate1)
                    run.append(Runtime1)
                    genre.append(Genre1)
                    imd.append(IMDB_Rating1)
                    over.append(Overview1)
                    meta.append(Meta_score1)
                    dir.append(Director1)
                    star_=[Star11,Star21,Star31,Star41]
                    stars.append(star_)
                    votes.append(No_of_Votes1)
                    gr.append(Gross1)
        clicked = clickable_images(
            link,
            titles=title,
            div_style={"display": "flex", "justify-content": "left", "flex-wrap": "wrap"},
            img_style={"margin": "5px", "height": "200px"},
        )
        st.markdown(f"Image #{clicked} clicked" if clicked > -1 else "No image clicked")
        for i in range(0,len(link)):
            if clicked==i:
                my_string = ', '.join(stars[i])
                my_string = my_string.replace('[','').replace(']','')
                print_stars(imd[i])
                val=f'''<p style="text-align:left">Title:{title[i]}</p>
                    <p style="text-align:left">Released Year:{rel[i]}</p>
                    <p style="text-align:left">Certificate:{cer[i]}</p>
                    <p style="text-align:left">Runtime:{run[i]}</p>
                    <p style="text-align:left">Cast:{my_string}</p>
                    <p style="text-align:left">Genre:{genre[i]}</p>
                    <p style="text-align:left">IMDB Rating:{imd[i]}</p>
                    <p style="text-align:left">Overview:{over[i]}</p>
                    <p style="text-align:left">Meta Score:{meta[i]}</p>
                    <p style="text-align:left">Director:{dir[i]}</p>
'''
                st.markdown(val,unsafe_allow_html=True)
    elif options=='IMDB_Rating':
        page_bg_img = f"""
        <style>
        [data-testid="stAppViewContainer"] > .main {{
        background-image: url("https://wallpapercave.com/dwp2x/wp6797747.gif");
        background-size: 100%;
        background-position: top left;
        background-repeat: no-repeat;
        background-attachment: local;
        }}
        [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
        }}
        [data-testid="stToolbar"] {{
        right: 2rem;
        }}
        </style>
        """
        st.markdown(page_bg_img, unsafe_allow_html=True)
        q2=f'''select * from  theater1.imdb1000 ORDER BY IMDB_Rating DESC limit 0,10'''
        cur.execute(q2)
        res1 = cur.fetchall()
        top_10 = '<p style="font-family:Copperplate, Papyrus, fantasy; color:#FFFFFF; font-size: 30px;text-align:center;"><b><u>TOP 10 ACCORDING TO IMDB Rating</u></b></p>'
        st.markdown(top_10, unsafe_allow_html=True)
        for i in range(0,len(res)):
            Poster_Link1   = res[i][0]
            Series_Title1  = res[i][1]
            Released_Year1 = res[i][2]
            Certificate1   = res[i][3]
            Runtime1       = res[i][4]
            Genre1         = res[i][5]
            IMDB_Rating1   = res[i][6]
            Overview1      = res[i][7]
            Meta_score1    = res[i][8]
            Director1      = res[i][9]
            Star11         = res[i][10]
            Star21         = res[i][11]
            Star31         = res[i][12]
            Star41         = res[i][13]
            No_of_Votes1   = res[i][14]
            Gross1         = res[i][15]
            for j in range(0,len(res1)):
                if(Poster_Link1 ==res1[j][0]):
                    link.append(Poster_Link1)
                    title.append(Series_Title1)
                    star_=[Star11,Star21,Star31,Star41]
                    stars.append(star_)
                    imd.append(IMDB_Rating1)
        clicked = clickable_images(
            link,
            titles=title,
            div_style={"display": "flex", "justify-content": "left", "flex-wrap": "wrap"},
            img_style={"margin": "5px", "height": "200px"},
        )
        st.markdown(f"Image #{clicked} clicked" if clicked > -1 else "No image clicked")
        for i in range(0,len(link)):
            if clicked==i:
                my_string = ', '.join(stars[i])
                my_string = my_string.replace('[','').replace(']','')
                print_stars(imd[i])
                val=f'''<p style="text-align:left">Title:{title[i]}</p>
                        <p style="text-align:left">Cast:{my_string}</p>'''
                st.markdown(val,unsafe_allow_html=True)
    elif options=='Director':
        page_bg_img = f"""
        <style>
        [data-testid="stAppViewContainer"] > .main {{
        background-image: url("https://www.filmibeat.com/ph-big/2012/01/nanban_13258339245.jpg");
        background-size: 100%;
        background-position: top left;
        background-repeat: no-repeat;
        background-attachment: local;
        }}
        [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
        }}
        [data-testid="stToolbar"] {{
        right: 2rem;
        }}
        </style>
        """
        st.markdown(page_bg_img, unsafe_allow_html=True)
        for i in range(0,len(res)):
            dir.append(res[i][9])
        drop_=st.selectbox('Director',(dir))
        st.write(drop_)
        q6=f'''select * from  theater1.imdb1000 WHERE Director="{drop_}"'''
        cur.execute(q6)
        res5 = cur.fetchall()
        top_10 = '<p style="font-family:Copperplate, Papyrus, fantasy; color:#FFFFFF; font-size: 30px;text-align:center;"><b><u>MOVIES FROM THE DIRECTOR</u></b></p>'
        st.markdown(top_10, unsafe_allow_html=True)
        for i in range(0,len(res)):
            Poster_Link1   = res[i][0]
            Series_Title1  = res[i][1]
            Released_Year1 = res[i][2]
            Certificate1   = res[i][3]
            Runtime1       = res[i][4]
            Genre1         = res[i][5]
            IMDB_Rating1   = res[i][6]
            Overview1      = res[i][7]
            Meta_score1    = res[i][8]
            Director1      = res[i][9]
            Star11         = res[i][10]
            Star21         = res[i][11]
            Star31         = res[i][12]
            Star41         = res[i][13]
            No_of_Votes1   = res[i][14]
            Gross1         = res[i][15]
            for j in range(0,len(res5)):
                if(Poster_Link1 ==res5[j][0]):
                    link.append(Poster_Link1)
                    title.append(Series_Title1)
                    rel.append(Released_Year1)
                    cer.append(Certificate1)
                    run.append(Runtime1)
                    genre.append(Genre1)
                    imd.append(IMDB_Rating1)
                    over.append(Overview1)
                    meta.append(Meta_score1)
                    dir.append(Director1)
                    star_=[Star11,Star21,Star31,Star41]
                    stars.append(star_)
                    votes.append(No_of_Votes1)
                    gr.append(Gross1)
        clicked = clickable_images(
            link,
            titles=title,
            div_style={"display": "flex", "justify-content": "left", "flex-wrap": "wrap"},
            img_style={"margin": "5px", "height": "200px"},
        )       
        st.markdown(f"Image #{clicked} clicked" if clicked > -1 else "No image clicked")
        for i in range(0,len(link)):
            if clicked==i:
                my_string = ', '.join(stars[i])
                my_string = my_string.replace('[','').replace(']','')
                print_stars(imd[i])
                val=f'''<p style="text-align:left">Title:{title[i]}</p>
                    <p style="text-align:left">Released Year:{rel[i]}</p>
                    <p style="text-align:left">Certificate:{cer[i]}</p>
                    <p style="text-align:left">Runtime:{run[i]}</p>
                    <p style="text-align:left">Genre:{genre[i]}</p>
                    <p style="text-align:left">Cast:{my_string}</p>
                    <p style="text-align:left">IMDB Rating:{imd[i]}</p>
                    <p style="text-align:left">Overview:{over[i]}</p>
                    <p style="text-align:left">Meta Score:{meta[i]}</p>
                    <p style="text-align:left">Director:{dir[i]}</p>
'''
                st.markdown(val,unsafe_allow_html=True)
    elif options=='Stars':
        page_bg_img = f"""
        <style>
        [data-testid="stAppViewContainer"] >.main {{
        background-image: url("https://w0.peakpx.com/wallpaper/982/205/HD-wallpaper-tom-holland-in-spiderman-homecoming-spiderman-homecoming-spiderman-2017-movies-movies-tom-holland.jpg");
        background-size: 100%;
        background-position: top left;
        background-attachment: local;
        }}
        [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
        }}
        [data-testid="stToolbar"] {{
        right: 2rem;
        }}
        </style>
        """
        st.markdown(page_bg_img, unsafe_allow_html=True)
        for i in range(0,len(res)):
            Poster_Link1   = res[i][0]
            Series_Title1  = res[i][1]
            Released_Year1 = res[i][2]
            Certificate1   = res[i][3]
            Runtime1       = res[i][4]
            Genre1         = res[i][5]
            IMDB_Rating1   = res[i][6]
            Overview1      = res[i][7]
            Meta_score1    = res[i][8]
            Director1      = res[i][9]
            Star11         = res[i][10]
            Star21         = res[i][11]
            Star31         = res[i][12]
            Star41         = res[i][13]
            No_of_Votes1   = res[i][14]
            Gross1         = res[i][15]
            star_=[Star11,Star21,Star31,Star41]
            stars.extend(star_) 
        unique_list=sorted(list(set(stars)))
        selected_option=st.selectbox('Select the actor whose movies you want to watch:',unique_list)
        q8=f'''select * from  theater1.imdb1000 WHERE Star1="{selected_option}" or Star2="{selected_option}" or Star3="{selected_option}" or Star4="{selected_option}"'''
        cur.execute(q8)
        res9 = cur.fetchall()
        stars=[]
        for i in range(0,len(res)):
            Poster_Link1   = res[i][0]
            Series_Title1  = res[i][1]
            Released_Year1 = res[i][2]
            Certificate1   = res[i][3]
            Runtime1       = res[i][4]
            Genre1         = res[i][5]
            IMDB_Rating1   = res[i][6]
            Overview1      = res[i][7]
            Meta_score1    = res[i][8]
            Director1      = res[i][9]
            Star11         = res[i][10]
            Star21         = res[i][11]
            Star31         = res[i][12]
            Star41         = res[i][13]
            No_of_Votes1   = res[i][14]
            Gross1         = res[i][15]
            for j in range(0,len(res9)):
                if(Poster_Link1 ==res9[j][0]):
                    link.append(Poster_Link1)
                    title.append(Series_Title1)
                    rel.append(Released_Year1)
                    cer.append(Certificate1)
                    run.append(Runtime1)
                    genre.append(Genre1)
                    imd.append(IMDB_Rating1)
                    over.append(Overview1)
                    meta.append(Meta_score1)
                    dir.append(Director1)
                    star_=[Star11,Star21,Star31,Star41]
                    stars.append(star_)
                    votes.append(No_of_Votes1)
                    gr.append(Gross1)
        clicked = clickable_images(
            link,
            titles=title,
            div_style={"display": "flex", "justify-content": "left", "flex-wrap": "wrap"},
            img_style={"margin": "5px", "height": "200px"},
        )       
        st.markdown(f"Image #{clicked} clicked" if clicked > -1 else "No image clicked")
        for i in range(0,len(link)):
            if clicked==i:
                my_string = ', '.join(stars[i])
                my_string = my_string.replace('[','').replace(']','')
                print_stars(imd[i])
                val=f'''<p style="text-align:left">Title:{title[i]}</p>
                    <p style="text-align:left">Released Year:{rel[i]}</p>
                    <p style="text-align:left">Certificate:{cer[i]}</p>
                    <p style="text-align:left">Runtime:{run[i]}</p>
                    <p style="text-align:left">Genre:{genre[i]}</p>
                    <p style="text-align:left">Cast:{my_string}</p>
                    <p style="text-align:left">IMDB Rating:{imd[i]}</p>
                    <p style="text-align:left">Overview:{over[i]}</p>
                    <p style="text-align:left">Meta Score:{meta[i]}</p>
                    <p style="text-align:left">Director:{dir[i]}</p>
'''
                st.markdown(val,unsafe_allow_html=True)

elif(add_sidebar=='Genre'):   
    q23=f'''select * from theater1.imdb'''
    cur.execute(q23)
    res = cur.fetchall()
    link=[]
    title=[]
    rel=[]
    cer=[]
    run=[]
    genre=[]
    imd=[]
    over=[]
    meta=[]
    dir=[]
    stars=[]
    votes=[]
    gr=[]
    movies=[]
    stars=[]
    gen_=[]
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] >.main {{
    background-image: url("https://moviegalleri.net/wp-content/uploads/2022/10/Actress-Ritu-Varma-in-Nitham-Oru-Vaanam-Movie-HD-Pics.jpg");
    background-size: 100%;
    background-position: top left;
        background-attachment: local;
        }}
        [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
        }}
        [data-testid="stToolbar"] {{
        right: 2rem;
        }}
        </style>
        """
    st.markdown(page_bg_img, unsafe_allow_html=True)
    tab1,tab2=st.tabs(['Your selection','Our selection'])
    l1=[]
    for i in range(0,len(res)):
            Poster_Link1   = res[i][0]
            Series_Title1  = res[i][1]
            Released_Year1 = res[i][2]
            Certificate1   = res[i][3]
            Runtime1       = res[i][4]
            Genre1         = res[i][5]
            IMDB_Rating1   = res[i][6]
            Overview1      = res[i][7]
            Meta_score1    = res[i][8]
            Director1      = res[i][9]
            Star11         = res[i][10]
            Star21         = res[i][11]
            Star31         = res[i][12]
            Star41         = res[i][13]
            No_of_Votes1   = res[i][14]
            Gross1         = res[i][15]
            star_=[Star11,Star21,Star31,Star41]
            stars.append(star_)
            gen = Genre1.split(',')
            gen_.extend(gen)
            movie_dict={'name':Series_Title1,'Genres1':gen,'URL':Poster_Link1,'STars':stars,'Rel':Released_Year1,'Over':Overview1,'Direc':Director1,'IM':IMDB_Rating1}
            movies.append(movie_dict)    
    with tab1:
        matching_movies=[]
        urls=[]
        summary=[]
        rel=[]
        dirr=[]
        gen4=[]
        genre=['Action ','Adventure' ,'Animation' ,'Biography' ,'Comedy' ,'Crime' ,'Drama' ,'Family' ,'Fantasy' ,'Film-Noir' ,'History' ,'Horror' ,'Music' ,'Musical' ,'Mystery' ,'Romance' ,'Sci-Fi' ,'Thriller' ,'War' ,'Western']
        st.markdown("<h2>Based on genre",unsafe_allow_html=True)
        m=st.multiselect('Genre u want:',genre)
        st.write('i want ',*m)
        for movie in movies:
            for genre in m:
                if genre in movie['Genres1']:
                    matching_movies.append(movie['name'])
                    urls.append(movie['URL'])
                    summary.append(movie['Over'])
                    rel.append(movie['Rel'])
                    dirr.append(movie['Direc'])
                    gen4.append(movie['Genres1'])
                    imd.append(movie['IM'])
                    break    
        clicked = clickable_images(
                urls,
                titles=matching_movies,
                div_style={"display": "flex", "justify-content": "left", "flex-wrap": "wrap"},
                img_style={"margin": "5px", "height": "200px"},
            )       
        st.markdown(f"Image #{clicked} clicked" if clicked > -1 else "No image clicked")
        for i in range(0,len(urls)):
            if clicked==i:
                    print_stars(imd[i])
                    val=f'''<p style="text-align:left">Title:{matching_movies[i]}</p>
                        <p style="text-align:left">Released Year:{rel[i]}</p>
                        <p style="text-align:left">Genre:{gen4[i]}</p>
                        <p style="text-align:left">Overview:{summary[i]}</p>
                        <p style="text-align:left">Director:{dirr[i]}</p>
                '''
                    st.markdown(val,unsafe_allow_html=True)

    with tab2:
        matching_movies=[]
        urls=[]
        summary=[]
        rel=[]
        dirr=[]
        gen4=[]
        st.title("How are you feeling today?")
        st.write("Select your mood using the emojis below:")

        # Define a dictionary of mood options
        mood_options = {
            "😃": "Happy",
            "😠": "Angry",
            "😴": "Tired",
        }

        # Add a radio button to let the user select their mood
        mood = st.radio("", options=list(mood_options.keys()))

        # Recommend movies based on the user's selected mood
        if mood:
            st.write(f"You selected {mood_options[mood]}")
            if mood == "😠":
                m=["Action"]
            elif mood == "😃":
                m=["Adventure","Comedy"]
            elif mood == "😴":
                m=["Mystery","Drama"]
        
        for movie in movies:
            for genre in m:
                if genre in movie['Genres1']:
                    matching_movies.append(movie['name'])
                    urls.append(movie['URL'])
                    summary.append(movie['Over'])
                    rel.append(movie['Rel'])
                    dirr.append(movie['Direc'])
                    gen4.append(movie['Genres1'])
                    imd.append(movie['IM'])
                    break    
        clicked = clickable_images(
                urls,
                titles=matching_movies,
                div_style={"display": "flex", "justify-content": "left", "flex-wrap": "wrap"},
                img_style={"margin": "5px", "height": "200px"},key="jfeijf"
            )       
        st.markdown(f"Image #{clicked} clicked" if clicked > -1 else "No image clicked")
        for i in range(0,len(urls)):
            if clicked==i:
                    print_stars(imd[i])
                    val=f'''<p style="text-align:left">Title:{matching_movies[i]}</p>
                        <p style="text-align:left">Released Year:{rel[i]}</p>
                        <p style="text-align:left">Genre:{gen4[i]}</p>
                        <p style="text-align:left">Overview:{summary[i]}</p>
                        <p style="text-align:left">Director:{dirr[i]}</p>
                '''
                    st.markdown(val,unsafe_allow_html=True)
elif(add_sidebar=='Rate'):
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] >.main {{
    background-image: url("https://cdn-icons-png.flaticon.com/512/2660/2660518.png");
    background-size: 100%;
    background-position: top left;
        background-attachment: local;
        }}
        [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
        }}
        [data-testid="stToolbar"] {{
        right: 2rem;
        }}
        </style>
        """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Create a form to ask for feedback
    with st.form(key='feedback_form'):
        st.write("Did you enjoy the app?")
        feedback = st.selectbox('', ('Yes', 'No'))
        if feedback == 'No':
            st.write('Can you give us your feedback?')
            reason = st.text_area('')
            with st.spinner('Loading...'):
                time.sleep(7)
                st.success("🎈We are very sorry for the inconvenience .We will take your suggestion into account and improve it to fit your preference🎈")    
        else:
            st.markdown(":smile_cat:... 🐰...🐇 ")
        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        st.write("Thank you for visiting our website")
        
    mydb.close()