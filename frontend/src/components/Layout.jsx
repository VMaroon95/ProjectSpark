function Layout({ activeTab, onTabChange, children }) {
    const tabs = [
        { key: 'dashboard', label: 'Dashboard', icon: '📊' },
        { key: 'heatmap', label: 'Model Robustness', icon: '🗺️' },
        { key: 'sweep', label: 'Sweep Results', icon: '📈' },
        { key: 'audit', label: 'Copyright Audit', icon: '🔍' },
        { key: 'disclosure', label: 'Disclosure Form', icon: '📄' },
    ];

    return React.createElement('div', { className: 'layout' },
        React.createElement('nav', { className: 'sidebar' },
            React.createElement('div', { className: 'logo' },
                React.createElement('span', { className: 'logo-icon' }, '⚡'),
                React.createElement('span', { className: 'logo-text' }, 'ProjectSpark'),
            ),
            React.createElement('div', { className: 'nav-links' },
                ...tabs.map(tab =>
                    React.createElement('button', {
                        key: tab.key,
                        className: 'nav-btn' + (activeTab === tab.key ? ' active' : ''),
                        onClick: () => onTabChange(tab.key),
                    },
                        React.createElement('span', { className: 'nav-icon' }, tab.icon),
                        React.createElement('span', null, tab.label),
                    )
                )
            ),
            React.createElement('div', { className: 'sidebar-footer' },
                React.createElement('p', null, 'AI Governance Platform'),
                React.createElement('p', { className: 'version' }, 'v1.0.0'),
            ),
        ),
        React.createElement('main', { className: 'content' }, children),
    );
}
window.Layout = Layout;
