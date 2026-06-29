import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './Card';

interface KpiCardProps {
  title: string;
  value: string | number;
  changePercent?: number;
  comparisonPeriod?: string;
  isLoading?: boolean;
  isError?: boolean;
  trend?: 'up' | 'down' | 'neutral';
}

const KpiCard: React.FC<KpiCardProps> = ({
  title,
  value,
  changePercent,
  comparisonPeriod,
  isLoading,
  isError,
  trend,
}) => {
  if (isLoading) {
    return (
      <Card>
        <CardHeader className="pb-2">
          <div className="h-4 w-1/2 bg-muted rounded animate-pulse"></div>
        </CardHeader>
        <CardContent>
          <div className="h-8 w-3/4 bg-muted rounded animate-pulse mt-2"></div>
          <div className="h-3 w-1/3 bg-muted rounded animate-pulse mt-4"></div>
        </CardContent>
      </Card>
    );
  }

  if (isError) {
    return (
      <Card className="border-destructive">
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-medium text-muted-foreground font-inter">{title}</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-sm text-destructive mt-2">Failed to load data</div>
        </CardContent>
      </Card>
    );
  }

  const isPositive = trend === 'up' || (changePercent && changePercent > 0);
  const isNegative = trend === 'down' || (changePercent && changePercent < 0);
  
  let trendClass = 'text-muted-foreground';
  if (isPositive) trendClass = 'text-accent';
  if (isNegative) trendClass = 'text-destructive';

  return (
    <Card>
      <CardHeader className="pb-2 flex flex-row items-center justify-between space-y-0">
        <CardTitle className="text-sm font-medium text-muted-foreground font-inter">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold font-orbitron">{value}</div>
        <div className="flex items-center gap-2 mt-2 text-xs">
          {changePercent !== undefined && (
            <span className={`font-semibold ${trendClass}`}>
              {isPositive && '↑ '}
              {isNegative && '↓ '}
              {Math.abs(changePercent)}%
            </span>
          )}
          {comparisonPeriod && (
            <span className="text-muted-foreground">vs {comparisonPeriod}</span>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default KpiCard;
