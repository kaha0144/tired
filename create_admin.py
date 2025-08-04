import argparse
from app import app, db, User, generate_password_hash

def create_user(username, nickname, password, is_admin=False):
    """新しいユーザーを作成してデータベースに保存する関数"""
    with app.app_context():
        # ユーザーが既に存在するかチェック
        if User.query.filter_by(username=username).first():
            print(f"エラー: ユーザー名 '{username}' は既に存在します。")
            return

        # パスワードをハッシュ化
        hashed_password = generate_password_hash(
            password,
            method="pbkdf2:sha256"
        )
        
        # 新しいユーザーオブジェクトを作成
        new_user = User(
            username=username,
            nickname=nickname,
            password=hashed_password,
            is_admin=is_admin
        )
        
        # データベースに保存
        db.session.add(new_user)
        db.session.commit()
        
        admin_text = " (管理者)" if is_admin else ""
        print(f"成功: ユーザー '{nickname}'{admin_text} が作成されました。")

if __name__ == '__main__':
    # コマンドラインから引数を受け取る設定
    parser = argparse.ArgumentParser(description='新しいユーザーを作成します。')
    parser.add_argument('username', type=str, help='ログインIDとなるユーザー名')
    parser.add_argument('nickname', type=str, help='表示されるニックネーム')
    parser.add_argument('password', type=str, help='ログインパスワード')
    parser.add_argument('--admin', action='store_true', help='このユーザーを管理者として作成する場合に指定します。')
    
    args = parser.parse_args()
    
    create_user(args.username, args.nickname, args.password, args.admin)