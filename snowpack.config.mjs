export default {
  optimize: {
    bundle: true,
    minify: false,
    target: 'es2020',
    entrypoints:[
      "WebActivities/07-Helios-web-simple/script.js",
      "WebActivities/08-Helios-web-complex/script.js"
    ],
  },
  devOptions: {
    openUrl: "WebActivities/08-Helios-web-complex/",
  },
  exlude:[
    '**/node_modules/**/*',
    '**/.git/**/*',
    '**/Activities/**/*'
  ],
  packageOptions:{
    external:[
    ]
  }
};
