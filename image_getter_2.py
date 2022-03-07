import image_to_db as to_db

def main():
        database = "/home/adam/sci/db/image_paths.db"

        conn = to_db.create_connection(database)

        with conn:
                print('hello')
                #image = ('path', '2020-10-14', '00', 'SD_N')
                #image_id = to_db.create_image(conn, image)

if __name__ == '__main__':
        main()
