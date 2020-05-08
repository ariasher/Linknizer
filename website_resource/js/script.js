
$(function () {
    const exceptions = ["desktop.ini", "index.html", "website_resource", "web.config"];

    $("#tree").fancytree({
        source: {
            url: "website_resource/listing.json",
            cache: true
        },
        cache: true,
        renderTitle: function (event, data) {
            if (!data.node.folder) {
                const node = data.node;
                const link = node.data.link;
                const title = node.title;
                const html = `<span><a href='${link}' class='link'>${title}</a></span>`;
                return html;
            }
        },
        renderNode: function (event, data) {
            const node = data.node;
            const title = node.title;
            const filtered_exception = exceptions.filter(function (exception) {
                return exception == title;
            });

            if (filtered_exception.length > 0) {
                $(node.span).closest("li").hide();
            }
        },
        icon: function (event, data) {
            const node = data.node;
            return node.folder ? "folder-icon fas fa-folder" : "file-icon fas fa-file";
        }
    });
});