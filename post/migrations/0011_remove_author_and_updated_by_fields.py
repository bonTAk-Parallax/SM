from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('post', '0010_comment_author_comment_updated_by_commentlike_author_and_more'),  
    ]

    operations = [

         # Remove duplicate fields from Post
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
        migrations.RemoveField(
            model_name='post',
            name='updated_by',
        ),
        # Remove duplicate fields from PostLike
        migrations.RemoveField(
            model_name='postlike',
            name='author',
        ),
        migrations.RemoveField(
            model_name='postlike',
            name='updated_by',
        ),
        # Remove duplicate author/updated_by fields from Comment
        migrations.RemoveField(
            model_name='comment',
            name='author',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='updated_by',
        ),

        # Remove duplicate author/updated_by fields from CommentLike
        migrations.RemoveField(
            model_name='commentlike',
            name='author',
        ),
        migrations.RemoveField(
            model_name='commentlike',
            name='updated_by',
        ),

        # Remove duplicate author/updated_by fields from Reply
        migrations.RemoveField(
            model_name='reply',
            name='author',
        ),
        migrations.RemoveField(
            model_name='reply',
            name='updated_by',
        ),

        # Remove duplicate author/updated_by fields from ReplyLike
        migrations.RemoveField(
            model_name='replylike',
            name='author',
        ),
        migrations.RemoveField(
            model_name='replylike',
            name='updated_by',
        ),
    ]
