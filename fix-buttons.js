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
        
        // If a class name contains bg-indigo-500 or bg-indigo-600, replace text-slate-900 with text-white
        newContent = newContent.replace(/className="([^"]*(bg-indigo-[56]00|bg-primary|from-indigo|bg-teal-[56]00|bg-rose-[56]00|bg-emerald-[56]00)[^"]*)"/g, function(match, innerClass) {
            return 'className="' + innerClass.replace(/text-slate-900/g, 'text-white') + '"';
        });

        // Also fix the Hero banner in App.tsx which was changed to bg-indigo-50 and might need special text handling
        // Well, bg-indigo-50 is very light, so text-slate-900 is correct there.

        if (content !== newContent) {
            fs.writeFileSync(filePath, newContent);
            console.log('Fixed buttons', filePath);
        }
    }
});
