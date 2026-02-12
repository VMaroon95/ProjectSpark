window.formatters = {
    percent(val) {
        return (val * 100).toFixed(1) + '%';
    },
    archName(key) {
        const names = {
            zero_shot: 'Zero-Shot',
            chain_of_thought: 'Chain-of-Thought',
            persona_based: 'Persona-Based',
            few_shot: 'Few-Shot',
            delimiter_heavy: 'Delimiter-Heavy',
        };
        return names[key] || key;
    },
    subjectName(key) {
        const names = {
            stem: 'STEM',
            humanities: 'Humanities',
            social_sciences: 'Social Sciences',
            other: 'Other',
        };
        return names[key] || key;
    },
    riskColor(level) {
        const colors = { high: '#f85149', medium: '#d29922', low: '#2ea043', unknown: '#8b949e' };
        return colors[level] || '#8b949e';
    },
    number(val) {
        return new Intl.NumberFormat().format(val);
    },
};
