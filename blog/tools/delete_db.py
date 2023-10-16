import sqlite3

# データベースに接続する
conn = sqlite3.connect('blog/instance/project.db')
c = conn.cursor()
c.execute('DELETE FROM user_info WHERE id=?', (4,))

#保存（コミット）する
conn.commit()

c.execute('select * from user_info')
print(c.fetchall())

#データベースへの接続を終了する
conn.close()