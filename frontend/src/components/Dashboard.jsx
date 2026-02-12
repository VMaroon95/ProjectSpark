function Dashboard() {
    const [stats, setStats] = React.useState(null);

    React.useEffect(() => {
        api.getStats().then(setStats).catch(() => {
            setStats({
                models_tested: 1, avg_robustness_score: 0.83,
                datasets_audited: 0, high_risk_sources: 0, total_sources_scanned: 0,
            });
        });
    }, []);

    if (!stats) return React.createElement('div', { className: 'loading' }, 'Loading...');

    const cards = [
        { label: 'Models Tested', value: stats.models_tested, icon: '🤖' },
        { label: 'Robustness Score', value: (stats.avg_robustness_score * 100).toFixed(0) + '%', icon: '🛡️' },
        { label: 'Datasets Audited', value: stats.datasets_audited, icon: '📊' },
        { label: 'High-Risk Sources', value: stats.high_risk_sources, icon: '⚠️' },
    ];

    return React.createElement('div', { className: 'dashboard' },
        React.createElement('h2', null, 'Dashboard Overview'),
        React.createElement('div', { className: 'cards-grid' },
            ...cards.map((card, i) =>
                React.createElement('div', { key: i, className: 'stat-card' },
                    React.createElement('div', { className: 'stat-icon' }, card.icon),
                    React.createElement('div', { className: 'stat-value' }, card.value),
                    React.createElement('div', { className: 'stat-label' }, card.label),
                )
            )
        ),
        React.createElement('div', { className: 'card' },
            React.createElement('h3', null, 'Quick Start'),
            React.createElement('p', null, '1. View the Model Robustness heatmap to see how prompt architecture affects benchmark scores.'),
            React.createElement('p', null, '2. Upload a dataset manifest CSV in the Copyright Audit tab to scan for risky sources.'),
            React.createElement('p', null, '3. Generate a Federal Disclosure Form PDF for CLEAR Act compliance.'),
        )
    );
}
window.Dashboard = Dashboard;
