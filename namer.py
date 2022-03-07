import os
import shutil

def main():
	location = '/var/www/html/images/'


	files = []
	##get just the files in the images directory
	for (dirpath, dirnames, filenames) in os.walk("/var/www/html/images"):
		files.extend(filenames)
		break
	##sort the files so that we can get the zero hour images
	files.sort(key=lambda x: x[::-5], reverse=True)
	files = files[:3]
	dir_names = []
	##get the directory names for the past files
	for f in files:
		name = f.split("s")
		dir_names.append(name[0])
		print(dir_names.append(name[0]))

	################## Move each file in the past folder twelve hours #################################
        #get list of files in ONE regions _past folder
	for dir_name in dir_names:
        	region_filename = os.listdir(location+dir_name+'_past')
		times = [84,72,60,48,36,24,12]
		region_filename.sort(reverse=True)
        	##For each time, add 12 hours and save file
        	for i, t in enumerate(times):
                	t = t + 12
			#print location+dir_name+'_past/'+region_filename[i+1], location+dir_name+'_past/'+dir_name+'surface_pressure-'+str(t)+'.png'
			shutil.copyfile(location+dir_name+'_past/'+region_filename[i+1], location+dir_name+'_past/'+dir_name+'surface_pressure-'+str(t)+'.png')
        ###################################################################################################

        ################## Copy 0 hour file to the past directory, and rename as -12 #######################
        for f in files:
                name = f.split("s")
                shutil.copyfile(location + f, location+name[0]+'_past/'+name[0]+'surface_pressure-12.png')
                print(f, name[0]+'_past/'+name[0]+'surface_pressure-12.png')

if __name__ == '__main__':
	main()
