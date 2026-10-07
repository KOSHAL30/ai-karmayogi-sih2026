const fs = require('fs');
const path = require('path');

function walkDir(dir, callback) {
    fs.readdirSync(dir).forEach(f => {
        let dirPath = path.join(dir, f);
        let isDirectory = fs.statSync(dirPath).isDirectory();
        isDirectory ? walkDir(dirPath, callback) : callback(path.join(dir, f));
    });
}

const colorReplacements = [
    { regex: /bg-slate-900|bg-slate-800|bg-slate-950/g, replacement: 'bg-white' },
    { regex: /dark:bg-slate-\d+/g, replacement: '' },
    { regex: /dark:text-slate-\d+/g, replacement: '' },
    { regex: /dark:text-white/g, replacement: '' },
    { regex: /dark:border-slate-\d+/g, replacement: '' },
    { regex: /dark:bg-[a-zA-Z0-9\-]+/g, replacement: '' },
    { regex: /dark:hover-[a-zA-Z0-9\-]+/g, replacement: '' },
    { regex: /dark:hover:\S+/g, replacement: '' },
    { regex: /text-slate-300|text-slate-400|text-slate-200/g, replacement: 'text-slate-600' },
    { regex: /text-white/g, replacement: 'text-slate-900' },
    { regex: /text-emerald-400|text-emerald-200/g, replacement: 'text-teal-700' },
    { regex: /text-amber-400|text-amber-200/g, replacement: 'text-amber-700' },
    { regex: /bg-emerald-500|bg-emerald-600/g, replacement: 'bg-indigo-500' },
    { regex: /hover:bg-emerald-500|hover:bg-emerald-600/g, replacement: 'hover:bg-indigo-600' },
    { regex: /text-emerald-500|text-emerald-600/g, replacement: 'text-teal-600' },
    { regex: /border-slate-700|border-slate-800/g, replacement: 'border-slate-200' },
    { regex: /bg-gradient-to-br from-\[#F97316\] via-\[#EA580C\] to-\[#C2410C\]/g, replacement: 'bg-indigo-50 border-indigo-100' },
    { regex: /bg-gradient-to-br from-\[#F97316\] to-\[#FB923C\]/g, replacement: 'bg-indigo-600' },
    { regex: /shadow-\[#F97316\]\/25/g, replacement: 'shadow-indigo-500/25' },
    { regex: /shadow-\[#F97316\]\/40/g, replacement: 'shadow-indigo-500/40' },
    { regex: /bg-gradient-to-r from-\[#FF9933\] via-white to-\[#138808\]/g, replacement: 'bg-indigo-600' },
    { regex: /bg-primary/g, replacement: 'bg-indigo-500' },
    { regex: /text-primary-foreground/g, replacement: 'text-white' }
];

walkDir('./frontend/src', function(filePath) {
    if (filePath.endsWith('.tsx') || filePath.endsWith('.ts')) {
        let content = fs.readFileSync(filePath, 'utf8');
        let newContent = content;
        
        for (const rule of colorReplacements) {
            newContent = newContent.replace(rule.regex, rule.replacement);
        }
        
        if (content !== newContent) {
            fs.writeFileSync(filePath, newContent);
            console.log('Updated', filePath);
        }
    }
});
