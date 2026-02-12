function HeatmapView() {
    const [data, setData] = React.useState(null);
    const [results, setResults] = React.useState(null);

    React.useEffect(() => {
        api.getHeatmap().then(setData).catch(() => {});
        api.getEvalResults().then(setResults).catch(() => {});
    }, []);

    if (!data) return React.createElement('div', { className: 'loading' }, 'Loading heatmap data...');

    const sa = results && results.sensitivity_analysis;

    return React.createElement('div', { className: 'heatmap-view' },
        React.createElement('h2', null, 'Model Robustness Heatmap'),
        React.createElement('p', { className: 'subtitle' },
            'Accuracy scores across prompt architectures and MMLU subject areas. ',
            results ? `Model: ${results.metadata.model}` : ''
        ),
        React.createElement(Heatmap, data),
        sa && React.createElement('div', { className: 'card stats-row' },
            React.createElement('div', { className: 'stat-item' },
                React.createElement('span', { className: 'stat-label' }, 'Robustness Score'),
                React.createElement('span', { className: 'stat-value' }, (sa.robustness_score * 100).toFixed(0) + '%'),
            ),
            React.createElement('div', { className: 'stat-item' },
                React.createElement('span', { className: 'stat-label' }, 'Most Sensitive Subject'),
                React.createElement('span', { className: 'stat-value' }, formatters.subjectName(sa.max_variance_subject)),
            ),
            React.createElement('div', { className: 'stat-item' },
                React.createElement('span', { className: 'stat-label' }, 'Best Architecture'),
                React.createElement('span', { className: 'stat-value' }, formatters.archName(sa.most_sensitive_architecture)),
            ),
            React.createElement('div', { className: 'stat-item' },
                React.createElement('span', { className: 'stat-label' }, 'Score Range'),
                React.createElement('span', { className: 'stat-value' }, (sa.overall_range * 100).toFixed(1) + ' pts'),
            ),
        ),
    );
}
window.HeatmapView = HeatmapView;
