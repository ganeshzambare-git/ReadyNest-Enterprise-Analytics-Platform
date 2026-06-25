import fs from 'fs';
import path from 'path';

const routes = [
  "data-ingestion",
  "data-quality",
  "data-cleaning",
  "descriptive-statistics",
  "univariate-analysis",
  "bivariate-analysis",
  "customer-overview",
  "customer-analysis",
  "customer-segmentation",
  "sales-performance",
  "product-performance",
  "behavior-analysis",
  "key-insights",
  "business-suggestions",
  "interactive-dashboard",
  "predictive-modeling",
  "advanced-visuals",
  "automated-reporting",
  "governance-security",
  "monitoring-observability",
  "cloud-integration",
];

const basePath = path.join(process.cwd(), 'src', 'app', 'services');

routes.forEach(route => {
  const dirPath = path.join(basePath, route);
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
  
  const title = route.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
  
  const content = `export default function ${title.replace(/\s+/g, '')}Page() {
  return (
    <div className="container mx-auto max-w-screen-2xl px-4 py-12">
      <h1 className="text-4xl font-bold tracking-tight mb-4">${title}</h1>
      <p className="text-muted-foreground text-lg">
        This is a placeholder for the ${title} enterprise module.
      </p>
    </div>
  )
}
`;
  
  fs.writeFileSync(path.join(dirPath, 'page.tsx'), content);
  console.log("Created route: " + route);
});
