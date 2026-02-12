function App() {
    const [tab, setTab] = React.useState('dashboard');

    const pages = {
        dashboard: React.createElement(Dashboard),
        heatmap: React.createElement(HeatmapView),
        sweep: React.createElement(SweepResults),
        audit: React.createElement(CopyrightAudit),
        disclosure: React.createElement(DisclosureForm),
    };

    return React.createElement(Layout, { activeTab: tab, onTabChange: setTab }, pages[tab]);
}
window.App = App;
