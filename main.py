#! /usr/bin/env python

from sugar.activity import activity
import sys, os, subprocess
import gtk, gobject, pango
import logging
from gettext import gettext as _
from sugar.graphics.objectchooser import ObjectChooser
import sugar.graphics.toolbutton
from sugar import mime
import id3reader




class Radio(activity.Activity):

	def __init__(self, handle):

		activity.Activity.__init__(self, handle)	


		toolbox = activity.ActivityToolbox(self)

		self.set_toolbox(toolbox)



		toolbox.show()
 		box_canvas = gtk.VBox(False, 0)
        	self.set_canvas(box_canvas)


        	# Title

        	box_title = gtk.VBox(False, 0)
        	self.label_title = gtk.Label(_("Welcome to Radio!"))
        	self.label_title.set_justify(gtk.JUSTIFY_CENTER)
        	self.label_title.modify_font(pango.FontDescription("Sans 22"))
	
        	box_title.add(gtk.Label("\n\n\n"))
        	box_title.add(self.label_title)
        	box_title.add(gtk.Label("\n"))

        	# playing

        	self.box_playing = gtk.VBox(False, 0)

        	self.label_playing_url = gtk.Label('Please open a file by selecting the "Open" or "Open from USB/SD" button in the toolbar.')
		self.box_playing.add(self.label_playing_url)	
        	self.label_playing_url.set_justify(gtk.JUSTIFY_CENTER)
        	self.label_playing_url.modify_font(pango.FontDescription("Sans 14"))
        	self.label_playing_url.set_line_wrap(True)
	
	        box_canvas.pack_start(box_title, False, False, 0)
	        box_canvas.pack_start(self.box_playing, False, False, 0)






		self.show_all()
		toolbox.get_activity_toolbar().keep.hide()
		toolbox.get_activity_toolbar().share.hide()
        	toolbox.get_activity_toolbar().remove(toolbox.get_activity_toolbar().share)
        	toolbox.get_activity_toolbar().remove(toolbox.get_activity_toolbar().keep)
        	self.sep1 = gtk.SeparatorToolItem()
        	self.sep1.set_expand(True)
        	self.sep1.set_draw(False)
		self.sep1.show()
        	toolbox.get_activity_toolbar().insert(self.sep1, 2)



       		self.play_button = sugar.graphics.toolbutton.ToolButton()


        	self.play_button.show()

        	self.pause_image = gtk.image_new_from_stock(gtk.STOCK_MEDIA_STOP,
                                                    gtk.ICON_SIZE_BUTTON)
        	self.pause_image.show()
        	self.play_image = gtk.image_new_from_stock(gtk.STOCK_MEDIA_PLAY,
                                                   gtk.ICON_SIZE_BUTTON)
        	self.play_image.show()

        	self.play_button.set_icon_widget(self.play_image)

        	self.play_button.connect('clicked', self._boton_apretado)
        	toolbox.get_activity_toolbar().insert(self.play_button, 2)
		self.play_button.set_tooltip(_('Play'))
        	self.sep1 = gtk.SeparatorToolItem()
        	self.sep1.set_expand(True)
        	self.sep1.set_draw(False)
		self.sep1.show()
        	toolbox.get_activity_toolbar().insert(self.sep1, 2)

	        self.usb_button = sugar.graphics.toolbutton.ToolButton("usb")
		self.usb_button.set_tooltip(_('Open from USB/SD'))
	
	        self.usb_button.show()


	        self.usb_button.connect('clicked', self.show_usb)
	        toolbox.get_activity_toolbar().insert(self.usb_button, 2)
	        self.open_button = sugar.graphics.toolbutton.ToolButton("stock-open")
		self.open_button.set_tooltip(_('Open'))
		self.open_button.props.accelerator="<Ctrl>O"
	        self.open_button.show()


	        self.open_button.connect('clicked', self._show_picker_cb)
	        toolbox.get_activity_toolbar().insert(self.open_button, 2)
		


	def checkobj(self,blah,blah2):

		try:
        		self._is_jornal
		except AttributeError:
		
	       		self._show_picker_cb(self)	
	def _stop(self, widget, data=None):
		subprocess.Popen(['/usr/bin/killall','mpg123'])
        	self.play_button.set_icon_widget(self.play_image)
        	self.play_button.connect('clicked', self._boton_apretado)
		self.play_button.set_tooltip(_('Play'))
		#self.play_button.emit("clicked")
	def _boton_apretado(self, widget, data=None):

		#print "boton_apretado"

		#print self._is_jornal
		#print self._playingjnl
		if str(self._playingjnl).endswith(".mp3"):
			cmd = [  os.environ.get('SUGAR_BUNDLE_PATH')+"/bin/mpg123",str(self._playingjnl)]
		else:
			cmd = [  os.environ.get('SUGAR_BUNDLE_PATH')+"/bin/mpg123", "-@",str(self._playingjnl)]
		#print str(cmd)
                subprocess.Popen(cmd)
        	self.play_button.connect('clicked', self._stop)
        	self.play_button.set_icon_widget(self.pause_image)
	def read_file(self,fileread):
		self.fileread=fileread
		gobject.timeout_add(100,self.realread)
	def realread(self):
		fileread=self.fileread
		#print str(self) + str(oop)+str(fileread)
		print fileread
		if str(fileread).endswith(".mp3"):
			cmd = [  os.environ.get('SUGAR_BUNDLE_PATH')+"/bin/mpg123",str(fileread)]
		else:
			cmd = [  os.environ.get('SUGAR_BUNDLE_PATH')+"/bin/mpg123", "-@",str(fileread)]
		#print "playing "+ str(fileread)
		self._is_jornal="yes"
		self._playingjnl=str(fileread)
                subprocess.Popen(cmd)

		if str(fileread).endswith(".pls"):
			id3,err = subprocess.Popen(["/bin/sh","-c", "cat "+ str(fileread)+" | grep Title1= | cut -d '=' -f2"], stdout = subprocess.PIPE).communicate()
		elif str(fileread).endswith(".mp3"):
			id3r=id3reader.Reader(str(fileread))
			id3="Title: "+str(id3r.getValue('title'))+"\nArtist: "+str(id3r.getValue('performer'))+"\nAlbum: "+str(id3r.getValue('album'))+""
			#print id3
			#id3=id3.capitalize()
		else:	
			id3tmp,err = subprocess.Popen(["/bin/sh","-c", "cat "+ str(fileread)], stdout = subprocess.PIPE).communicate()
			id3="M3U stream at "+id3tmp+""
		#print "id3 is "+str(id3)

		if id3 == "":
			id3 = "Unknown"
		
        	self.play_button.connect('clicked', self._stop)
        	self.play_button.set_icon_widget(self.pause_image)
		self.play_button.set_tooltip(_('Stop'))
        	self.box_playing.remove(self.label_playing_url)
        	self.label_playing_url = gtk.Label(str(id3))
        	self.label_playing_url.set_justify(gtk.JUSTIFY_CENTER)
        	self.label_playing_url.set_line_wrap(True)
        	self.label_playing_url.modify_font(pango.FontDescription("Sans 14"))
		self.box_playing.add(self.label_playing_url)
		self.label_title.set_text(_("Now Playing"))
		if fileread.endswith('.mp3'):
			id3title=str(id3r.getValue('performer'))+" - "+str(id3r.getValue('title'))
		else:
			id3title = id3
		print id3title
		print fileread
		# not quite working... doesnt update after 1st song!
		#self.set_title("Now Playing:\n"+str(id3title))	=
		self.show_all()

    	def datastore_write_cb(self):
        	pass


    	def close(self,  skip_save=False):
        	"Override the close method so we don't try to create a Journal entry."
		subprocess.Popen(['/usr/bin/killall','mpg123'])
        	activity.Activity.close(self,  True)
	def _show_picker_cb(self,duumy1):


        	chooser = ObjectChooser(parent=self, what_filter=mime.GENERIC_TYPE_AUDIO)
       	 	try:
            		result = chooser.run()
            		if result == gtk.RESPONSE_ACCEPT:
                		jobject = chooser.get_selected_object()
                		if jobject and jobject.file_path:
                    			#print jobject.file_path
					self.obj=jobject.file_path
					subprocess.call(['/usr/bin/killall','mpg123'])
                    			self.read_file(str(jobject.file_path))
        	finally:
            		chooser.destroy()
           		del chooser
	def show_usb(self,dummy1):
		dialog = gtk.FileChooserDialog("Open from USB/SD",
                               None,
                               gtk.FILE_CHOOSER_ACTION_OPEN,
                               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		dialog.set_default_response(gtk.RESPONSE_OK)
		dialog.set_current_folder("/media")	
	
		filter = gtk.FileFilter()
		filter.set_name("Audio")
		filter.add_mime_type("audio/x-scpls")
		filter.add_mime_type("audio/mpeg")
		filter.add_mime_type("audio/x-mpegurl")
		filter.add_pattern("*.pls")
		filter.add_pattern("*.m3u")
		filter.add_pattern("*.mp3")
		dialog.add_filter(filter)

		response = dialog.run()
		if response == gtk.RESPONSE_OK:
			subprocess.call(['/usr/bin/killall','mpg123'])
    			self.fileread=str(dialog.get_filename())
			self.realread()
		elif response == gtk.RESPONSE_CANCEL:
    			print 'Closed, no files selected'
		dialog.destroy()

