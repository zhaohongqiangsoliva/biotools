import { render } from "../preset/vue.js";
export const bridgeData = {
    "workspaceFolder": "file:///Users/soliva/Desktop/7_cloud/google_driver/biotools/web/imputation-pages",
    "serverRootDir": "",
    "previewFolderRelPath": "preview",
    "activeFileRelPath": "src/views/upload/index.vue",
    "mapFileRelPath": "src/views/upload/index.vue",
    "presetName": "vue",
    "workspaceFolderName": "imputation-pages"
};
export const preview = () => render(getMod);
const getMod = () => import("../../src/views/upload/index.vue");