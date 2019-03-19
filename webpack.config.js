function getStyleUse(bundleFilename) {
    return [
        {
            loader: 'file-loader',
            options: {
                name: bundleFilename,
                outputPath: "../static/css"
            },
        },
        {loader: 'extract-loader'},
        {loader: 'css-loader'},
        {
            loader: 'sass-loader',
            options: {
                includePaths: ['./node_modules'],
            }
        },
    ];
}


module.exports = [
    {
        entry: './static_src/scss/codex_list.scss',
        output: {
            // This is necessary for webpack to compile, but we never reference this js file.
            filename: 'style-bundle.js',
        },
        module: {
            rules: [{
                test: /codex_list.scss$/,
                use: getStyleUse('[name].css')
            }]
        }
    },
    {
        entry: './static_src/scss/codex_add.scss',
        output: {
            // This is necessary for webpack to compile, but we never reference this js file.
            filename: 'style-bundle.js',
        },
        module: {
            rules: [{
                test: /codex_add.scss$/,
                use: getStyleUse('[name].css')
            }]
        }
    },
    {
        entry: './static_src/scss/connexion.scss',
        output: {
            // This is necessary for webpack to compile, but we never reference this js file.
            filename: 'style-bundle.js',
        },
        module: {
            rules: [{
                test: /connexion.scss$/,
                use: getStyleUse('[name].css')
            }]
        }
    },
    {
        entry: './static_src/scss/information.scss',
        output: {
            // This is necessary for webpack to compile, but we never reference this js file.
            filename: 'style-bundle.js',
        },
        module: {
            rules: [{
                test: /information.scss$/,
                use: getStyleUse('[name].css')
            }]
        }
    },
    {
        entry: './static_src/scss/task_list.scss',
        output: {
            // This is necessary for webpack to compile, but we never reference this js file.
            filename: 'style-bundle.js',
        },
        module: {
            rules: [{
                test: /task_list.scss$/,
                use: getStyleUse('[name].css')
            }]
        }
    },
    {
        entry: './static_src/scss/task_todo_list.scss',
        output: {
            // This is necessary for webpack to compile, but we never reference this js file.
            filename: 'style-bundle.js',
        },
        module: {
            rules: [{
                test: /task_todo_list.scss$/,
                use: getStyleUse('[name].css')
            }]
        }
    },
    {
        entry: './static_src/scss/codex_details.scss',
        output: {
            // This is necessary for webpack to compile, but we never reference this js file.
            filename: 'style-bundle.js',
        },
        module: {
            rules: [{
                test: /codex_details.scss$/,
                use: getStyleUse('[name].css')
            }]
        }
    },
];