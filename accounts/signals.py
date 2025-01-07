from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from system_main.models import File
from homepage.models import Project

@receiver(post_save, sender=User)
def create_initial_file(sender, instance, created, **kwargs):
    if created:
        # Training code for the initial file
        paintingFence = """
paintingFence(フェンスを塗る問題)
長さ n のフェンスと k 色のペイントを使って、以下のルールに従ってフェンスを塗る方法を考えます：
1.	隣り合う列のうち、同じ色で塗られるのは最大で2列まで。
2.	全ての列が色で塗られている必要がある。
フェンスを塗る方法の数を求めてください。
例:
n=3, k=2 の場合：
結果: paintingFence(n,k)=6

"""
        climbingstairs ="""
階段の登り方(Climbing Stairs)
概要
長さ n の階段を1段または2段ずつ登る場合、何通りの方法で登れるかを求める問題です。

例:
入力: n=4
出力: 5(1段+1段+1段+1段、1段+2段+1段、2段+1段+1段、2段+2段、1段+1段+2段)
"""
        removeDuplicates="""
整数の配列 arr が与えられます。この配列の各数値は最大で2回までしか出現できません。
それ以上出現する場合は、条件を満たすように削除します。操作を実行した後の配列の長さを求めてください。

例:

配列 arr = [1, 1, 1, 2, 3, 3] の場合
出力: removeDuplicates(arr) = 5
説明: 数字 1 は3回出現しているため、1つ削除して [1, 1, 2, 3, 3] にします。
他の数字は条件を満たしているので削除の必要はありません。

配列 arr = [1, 1, 1, 1] の場合
出力: removeDuplicates(arr) = 2
説明: 数字 1 は4回出現しているため、2つ削除して [1, 1] にします。

この例を使ってください arr= [4, 3, 2, 5, 5, 6, 4, 4, 5, 5, 6, 3, 3, 3 , 2]
"""
        pair="""
問題
配列 arr の中で、すべての値を2つずつのペアにする方法を考えます。
ペアを作れない値は配列から削除してください。最終的な配列を返します。

例
入力:arr = [1, 1, 1, 2, 2, 3, 3, 3, 3]
出力:[1, 1, 2, 2, 3, 3, 3, 3]
処理後の配列: 「1」を1つ削除します(ペアを作れないため)。
"""
        project_data = [
            {"title": "paintingFence", "language": "py", "code": paintingFence},
            {"title": "Challenge: paintingFence", "language": "py", "code": climbingstairs},
            {"title": "removeDuplicates", "language": "py", "code": removeDuplicates},
            {"title": "Challenge: removeDuplicates", "language": "py", "code": pair},
        ]

        for project in project_data:
            # Create each project
            new_project = Project.objects.create(user=instance, title=project["title"], language=project["language"])
            # Create the associated file
            File.objects.create(project=new_project, file_name='Introduction', code=project["code"])
    