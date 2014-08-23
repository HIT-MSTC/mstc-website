$("#join_us").on('click', function(){
    $.Dialog({
        shadow: true,
        overlay: false,
        draggable: true,
        icon: '<span class="icon-bus"></span>',
        title: 'Draggable window',
        width: 500,
        padding: 10,
        content: 'This Window is draggable by caption.',
        onShow: function(){
            var content = '<form id="login-form-1">' +
                    '<label>Login</label>' +
                    '<div class="input-control text"><input type="text" name="login"><button class="btn-clear"></button></div>' +
                    '<label>Password</label>'+
                    '<div class="input-control password"><input type="password" name="password"><button class="btn-reveal"></button></div>' +
                    '<div class="input-control checkbox"><label><input type="checkbox" name="c1" checked/><span class="check"></span>Check me out</label></div>'+
                    '<div class="form-actions">' +
                    '<button class="button primary">Login to...</button>&nbsp;'+
                    '<button class="button" type="button" onclick="$.Dialog.close()">Cancel</button> '+
                    '</div>'+
                    '</form>';

            $.Dialog.title("User login");
            $.Dialog.content(content);
        }
    });
});