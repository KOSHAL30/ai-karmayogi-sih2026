const fs = require('fs');
const path = require('path');

function walkDir(dir, callback) {
    fs.readdirSync(dir).forEach(f => {
        let dirPath = path.join(dir, f);
        let isDirectory = fs.statSync(dirPath).isDirectory();
        isDirectory ? walkDir(dirPath, callback) : callback(path.join(dir, f));
    });
}

walkDir('./frontend/src', function(filePath) {
    if (filePath.endsWith('.tsx') || filePath.endsWith('.ts')) {
        let content = fs.readFileSync(filePath, 'utf8');
        let newContent = content;
        
        // Remove lingering dark: classes completely
        newContent = newContent.replace(/dark:[a-zA-Z0-9\-\/\[\]#]+/g, '');

        // Replace the dark banner gradients with light variants
        newContent = newContent.replace(/from-slate-950 via-emerald-950 to-slate-900/g, 'from-indigo-50 via-white to-teal-50');
        newContent = newContent.replace(/from-slate-950 via-slate-900 to-emerald-950/g, 'from-indigo-50 via-white to-teal-50');
        newContent = newContent.replace(/from-emerald-900 via-slate-900 to-slate-900/g, 'from-indigo-50 via-white to-teal-50');
        newContent = newContent.replace(/from-emerald-900 via-emerald-950 to-slate-900/g, 'from-indigo-50 via-white to-teal-50');
        newContent = newContent.replace(/from-slate-900 via-emerald-950 to-slate-900/g, 'from-indigo-50 via-white to-teal-50');
        
        // Also check if there's any other text-emerald-300 on these banners which makes it unreadable on light bg
        newContent = newContent.replace(/text-emerald-300/g, 'text-teal-700');
        newContent = newContent.replace(/text-emerald-400\/30/g, 'border-teal-200');
        newContent = newContent.replace(/border-emerald-400\/30/g, 'border-teal-200');

        if (content !== newContent) {
            fs.writeFileSync(filePath, newContent);
            console.log('Fixed gradients in', filePath);
        }
    }
});
