#import requierments 

import youtube_dl
# ----------------------
from telegram.ext import *
#-----------------------
from telegram import *
#-----------------------
from moviepy.editor import *
#-----------------------
import logging
#-----------------------
import re
#.......................
import os 
#------------------------
import warnings
#------------------


#receive the updates from Telegram and to deliver them to said dispatcher
bot = Bot(token="5585415565:AAEJ0Q0dXfBu2USLVayR9C3p8mIVvTfXdYE")
updater = Updater(token="5585415565:AAEJ0Q0dXfBu2USLVayR9C3p8mIVvTfXdYE" , use_context=True)

#interduce the dispatcher locally for quicker access
dispatcher = updater.dispatcher

#do basic configration for logging system
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

#A context manager that copies and restores the warnings filter upon exiting the context.
warnings.catch_warnings()

#ignore the warnings
warnings.simplefilter("ignore")
#__________________________________[/start]_______________________________________

def start(update, context) :
    #bot.send_sticker(chat_id=update.effective_chat.id , sticker ="AAMCAgADGQEAAgIVYHBeTyURu5R57uV-pG1ZMGWYUAADbwADwZxgDMsOfYvA3U1WGAg9lS4AAwEAB20AA_JRAAIeBA")
    YES_NO = ["YES  💚" , "NO  ❤️"]
    #get users first name
    user_first_name = bot.get_chat(update.effective_chat.id).first_name

    Yes_No_buttons = []

    # a loop which create a button for each of bot's functionalities
    
    for yes_Or_NO in YES_NO:
        Yes_No_buttons.append(InlineKeyboardButton(yes_Or_NO, callback_data = yes_Or_NO[: len(yes_Or_NO)-1].lower()))

    #it'll show the buttons on the screen 
    reply_markup=InlineKeyboardMarkup(build_menu(Yes_No_buttons, n_cols=2 )) 

    #button's explanaions 
    update.message.reply_text(
        f"Hello dear {user_first_name} \nDo you want to make a GIF ?  ",
        reply_markup=reply_markup
    )
    return YesNoClick
    

# make columns based on how we declared 
def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
    YesNo_menu_buttons = [buttons[i:i + n_cols] for i in range(0 , len(buttons), n_cols)]
    if header_buttons:
        YesNo_menu_buttons.insert(0, header_buttons)
    if footer_buttons:
        YesNo_menu_buttons.append(footer_buttons)
    return YesNo_menu_buttons



#dispatcher.add_handler(CommandHandler("start" , start))

#________________________________[YES_NO]_____________________________
def YES_NO_CLICK(update,context):
    query = update.callback_query

    
    if str(query.data).replace(" ","").lower() == "yes" :
        print("TRUE")
        Link_Upload = ["LINK " , "UPLOAD"]

        Link_Upload_buttons = []

        # a loop which create a button for each of bot's functionalities
        for Link_Or_Upload in Link_Upload:
            Link_Upload_buttons.append(InlineKeyboardButton(Link_Or_Upload, callback_data = Link_Or_Upload.lower()))
  
        #it'll show the buttons on the screen 
        reply_markup=InlineKeyboardMarkup(Link_build_menu(Link_Upload_buttons, n_cols=2 )) 

        #button's explanaions 
        bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Do you Wanna Paste a Youtube Link or Upload a Video locally ?",
        reply_markup=reply_markup
        )
        return UPLOAD_LINK_CLICK
    
    if str(query.data).replace(" ","").lower()== "no❤"  :
        bot.send_message(chat_id=update.effective_chat.id,text="OK .... Have a nice day ! ")
        return quit(update,context)

    

# make columns based on how we declared 
def Link_build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
    Link_Upload_menu_buttons = [buttons[i:i + n_cols] for i in range(0 , len(buttons), n_cols)]
    if header_buttons:
        Link_Upload_menu_buttons.insert(0, header_buttons)
    if footer_buttons:
        Link_Upload_menu_buttons.append(footer_buttons)
    return Link_Upload_menu_buttons



def Upload_LINK_CLICK(update,context):
    query = update.callback_query
    if str(query.data).replace(" ","").lower() == "link" :
        bot.send_message(chat_id=update.effective_chat.id , text = "Great ❤️\nPlease Enter The Video Link ... ")
        return DOWNLOADER
    if str(query.data).replace(" ","").lower() == "upload":
        bot.send_message(chat_id=update.effective_chat.id , text = "Great ❤️\nPlease Upload your video file here (make sure you upload it as a video file) ... ")
        return DOWNLOADER


    


def downloader(update , context) :
    #print(str(update.message).split())
    print(str(update.message).strip())
    #for i in str(update.message).split():
       # print(i)

    if "'document':" in str(update.message).split() :
        if update.message.document.mime_type[:update.message.document.mime_type.index("/")] == "video":
           # FormatVid =  update.message.document.mime_type[update.message.document.mime_type.index("/")+1:]
            vid = update.message.document
            bot.get_file(vid).download("Video.mp4")
            context.user_data["video"] = "Video.mp4"

        else :
            bot.send_message(chat_id=update.effective_chat.id , text = "Unsupported Video Format ...\n")
            return quit(update,context)

        print("DOC")
        
        #print(True)
    if "'video':" in str(update.message).split() :
       # print("VID")
        video = update.message.video
        bot.get_file(video).download("Video.mp4")
        context.user_data["video"] = "Video.mp4"
        #print(True)
    if "'text':" in str(update.message).split():
        print(False)
        try : 
            link = update.message.text
            print(link)
            
            ydl_opts = {
                'outtmpl': 'video',
                'format' : "worstvideo/worst"
                }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
            


            print("h")
           # format_vid=re.sub(Video.mime_type[:Video.mime_type.index("/")+1],"",Video.mime_type)  
            VideoNameFormat ="video" #f"{Video.title}.{format_vid}"
            context.user_data["video"]= VideoNameFormat
        except Exception as e :
            print(e)
            bot.send_message(chat_id = update.effective_chat.id  , text = "Oooops Something Went Wrong ! Make sure you typed the link correctly ")
            return quit(update,context)
 

    try : 
        
        clip = VideoFileClip(context.user_data["video"])
        context.user_data["clip"]= clip
        bot.sendMessage(chat_id=update.effective_chat.id , text=f"PLEASE ENTER THE START SECOND\n(It must be between 0 and {int(clip.duration)-1})\notherwise it'll be invalid")
        return STARTSECOND
    except Exception as e :
        print(e)
        bot.send_message(chat_id=update.effective_chat.id , text = "Ooops ! Some thing went Wrong ! ")
        return quit(update,context)
        
def start_second(update,context):
    try:
        StartSec = int(update.message.text)
    
        if StartSec >= 0 and StartSec <= int(context.user_data["clip"].duration)-1:
            context.user_data["START"] = StartSec
            dur=int(context.user_data["clip"].duration)
            print(dur)
            bot.send_message(chat_id=update.effective_chat.id , text =f"Great !\n PLEASE ENTER THE END SECOND\n (It must be between {int(StartSec)+1} and {int(StartSec)+16 if int(StartSec)+16 <= dur else dur }) \n otherwise it'll be invalid")
            return ENDSECOND
        else :
            durr =int(context.user_data["clip"].duration)-1
            bot.send_message(chat_id=update.effective_chat.id , text=f"INVALID START POINT (IT MUST BE EQUEL TO 0 OR GREATER  THAN 0 and LESS THAN {durr})" )
    except Exception as e :
        print(e)
        bot.send_message(chat_id=update.effective_chat.id , text = "Ooops Some thing Went Wrong ... Make sure You Entered a Valid start point ! ") 
        return quit(update,context)
def end_second(update,context):
    try:
        EndSec = int(update.message.text)
        StartSec = int(context.user_data["START"])
        dur = int(context.user_data["clip"].duration)
    
        if EndSec > context.user_data["START"] and EndSec <= context.user_data["START"]+15 and EndSec <= int(context.user_data["clip"].duration):
            context.user_data["END"] = EndSec
            

            bot.send_message(chat_id=update.effective_chat.id , text = "BRAVO !\nPLEASE ENTER YOUR GIF's NAME (IT CAN'T INCLUDE ESPACIELL CHARACHTERS!) ")
            return GIFNAME
        else :
            dur= int(context.user_data["clip"].duration)
            bot.sendMessage(chat_id=update.effective_chat.id , text= f"INVALID END POINT(It must be between {int(StartSec)+1} and {int(StartSec)+16 if int(StartSec)+16 <= dur else dur }) \n otherwise it'll be invalid)" )
            return quit(update,context)
    except Exception as e :
        print(e)
        bot.send_message(chat_id=update.effective_chat.id , text = "Ooops Some thing Went Wrong ... Make sure You Entered a Valid End point ! ") 
        return quit(update,context)
def gif_name(update , context):
    GIF_NAME = str(update.message.text)
    bot.send_message(chat_id=update.effective_chat.id , text = "Please wait ... the process may take time ... ")
    clip = context.user_data["clip"]
    start = context.user_data["START"]
    end = context.user_data["END"]
    clip = clip.subclip(start, end)
    Firstvideo=context.user_data["video"]
    # saving video clip as gif
    clip.write_gif(f"{GIF_NAME}.gif")

    bot.send_animation(chat_id = update.effective_chat.id , animation = open(f"{GIF_NAME}.gif","rb") )
    
    os.remove(f"{GIF_NAME}.gif")
    clip.close()
    os.remove(Firstvideo)
    
    return quit(update, context)
    
"""
# loading video dsa gfg intro video
        bot.send_message(chat_id=update.effective_chat.id , text = f"{Video.title} has Downloaded successfully ... ")
        bot.send_video(chat_id=update.effective_chat.id ,video=open(f"{Video.title}.{format_vid}" , 'rb'), supports_streaming=True)
      
        try:
            os.remove(f"{Video.title}.{format_vid}")

"""
def help(update , context):
    bot.send_message(chat_id = update.effective_chat.id , text = "This is Small Giffy ... I am here to help you generate your own GIFs  .... \nIf you want to generate your own GIF start with : /start \nIf You have any comment or want to help me to get better contact my developer : /ContactDeveloper ")
    return quit(update,context)

dispatcher.add_handler(CommandHandler("help" , help))



    
#from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
#ffmpeg_extract_subclip("video1.mp4", start_time, end_time, targetname="test.mp4")
def quit(update, context):
    bot.send_sticker(chat_id=update.effective_chat.id , sticker = "CAACAgIAAxkBAAICXWBwab5dXpxy6nsxk2RbnMnFakI9AAIfAANZu_wl6jl0G9k9NpkeBA")
    
    bot.send_message(chat_id = update.effective_chat.id , text = "If you want to generate your own GIF : /start")
    return ConversationHandler.END

YesNoClick = 0
UPLOAD_LINK_CLICK =1
DOWNLOADER = 2
STARTSECOND=3
ENDSECOND=4
GIFNAME= 5
"""
handle_converstation_upload=ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        YesNoClick:[ CallbackQueryHandler(YES_NO_CLICK)],
        UPLOAD_LINK_CLICK :[ CallbackQueryHandler(Upload_LINK_CLICK)] , 
        UPLOADER : [MessageHandler(Filters.all,callback=uploader)],
        STARTSECOND: [MessageHandler(Filters.text,callback=start_second)],
        ENDSECOND  : [MessageHandler(Filters.text,callback=end_second)],
        GIFNAME  : [MessageHandler(Filters.text,callback=gif_name)]

    },
    fallbacks=[CommandHandler('quit', quit)])

dispatcher.add_handler(handle_converstation_upload)
"""

handle_converstation_ask_link=ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        YesNoClick:[ CallbackQueryHandler(YES_NO_CLICK)],
        UPLOAD_LINK_CLICK :[ CallbackQueryHandler(Upload_LINK_CLICK)] , 
        DOWNLOADER : [MessageHandler((Filters.text | Filters.video | Filters.document) ,callback=downloader)],
        STARTSECOND: [MessageHandler(Filters.text,callback=start_second)],
        ENDSECOND  : [MessageHandler(Filters.text,callback=end_second)],
        GIFNAME  : [MessageHandler(Filters.text,callback=gif_name)]

    },
    fallbacks=[CommandHandler('quit', quit)])

dispatcher.add_handler(handle_converstation_ask_link)




"""
handle_converstation_using_Button=ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        YES_NO_CLICK: [CallbackQueryHandler(Click_Button)],
        ABOUT: [MessageHandler(Filters.text, callback=about)]

    },
    fallbacks=[CommandHandler('quit', quit)])

dispatcher.add_handler(handle_converstation_using_Button)
"""
def ContactDev(update,context):
   
    bot.send_contact(chat_id=update.effective_chat.id, contact= Contact(phone_number="+46 73 095 7299", first_name="Reihaneh"))

dispatcher.add_handler(CommandHandler("ContactDeveloper" , ContactDev))

#start the bot
updater.start_polling()

# starting info 
logging.info("Bot is awake .... ")

#stop the bot with ctrl+C
updater.idle()