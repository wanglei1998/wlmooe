/**
 * Created by King on 2020/4/21.
 */
$(function () {
    $(".delete-comment-btn").click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var comment_id = tr.attr('data-id');
        zlalert.alertConfirm({
            "msg":"您确定要删除这条评论吗？",
            'confirmCallback': function () {
                zlajax.post({
                    'url': '/cms/dcomment/',
                    'data':{
                        'comment_id': comment_id
                    },
                    'success': function (data) {
                        if(data['code'] == 200){
                            window.location.reload();
                        }else{
                            zlalert.alertInfo(data['message']);
                        }
                    }
                })
            }
        });
    });
});
