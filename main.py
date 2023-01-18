from flask import Flask, request, send_file, redirect, render_template, session
from pytube import YouTube
from io import BytesIO
import requests, json, os, time

app = Flask(__name__)
app.config['SECRET_KEY'] = '37158c0588a417e8577215c6'

@app.route('/')
def downloader_home():
  return render_template('index.html')
  
@app.route('/hubungi')
def hubungi_kami():
  if request.method == 'POST':
    return redirect('wa.me/81328303820')
  
# Index

@app.route('/tiktok')
def tiktok_home():
	return render_template('tiktok.html')
	
@app.route('/ttdownload', methods=['GET','POST'])
def download_tt():
	link = request.form['url']
	api = 'https://api.akuari.my.id/downloader/tiktoknowm?link='+link
	return render_template('tiktok_download.html', url=api)
	
@app.route('/titokmusik')
def tiktok_musik():
  return render_template('tiktok_musik.html')
	
@app.route('/ttmusic', methods=['GET','POST'])
def tt_musik():
  url = request.form['url']
  api = 'https://api.akuari.my.id/downloader/tiktokaudio?link='+url
  return render_template('tiktok_download_musik.html', link=api)
	
@app.route('/youtubemp3', methods=['GET','POST'])
def download_ytmp3():
  if request.method == 'POST':
    session['link'] = request.form['url']
    try:
      url = YouTube(session['link'])
      url.check_availability()
    except:
      return render_template('error.html')
    return render_template('ytmp3_download.html', url=url)
  return render_template('youtubemp3.html')
  
@app.route('/youtube_dl', methods=['GET','POST'])
def ytmp3_download():
  if request.method == 'POST':
    url = YouTube(session['link'])
    musik = url.streams.filter(only_audio=True).first().download()
    pth = musik.split('//')[-1]
    names = musik.replace('.mp4','')
    namefile = os.rename(musik,names+'.mp3')
    return send_file(
      pth,
      as_attachment=True,
      download_name=namefile,
      mimetype="audio/mp3",
      )
  return redirect(url_for(download_ytmp3))
	
@app.route('/youtube', methods=['GET','POST'])
def download_yt():
  if request.method == 'POST':
    session['link'] = request.form['url']
    try:
      url = YouTube(session['link'])
      url.check_availability()
    except:
      return render_template('error.html')
    return render_template('youtube_download.html', url=url)
  return render_template('youtube.html')
  
@app.route('/youtube_dl', methods=['GET','POST'])
def yt_download():
  if request.method == 'POST':
    buffer = BytesIO()
    url = YouTube(session['link'])
    itag = request.form.get('itag')
    video = url.streams.get_by_itag(itag)
    video.stream_to_buffer(buffer)
    buffer.seek(0)
    return send_file(
      buffer,
      as_attachment=True,
      download_name="download_video_yt.mp4",
      mimetype="video",
      )
  return redirect(url_for(download_yt))

if __name__ == '__main__':
	app.run(debug=True, port=8015)