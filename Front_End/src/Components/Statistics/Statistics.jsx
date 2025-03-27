import * as React from 'react';
import { PieChart } from '@mui/x-charts/PieChart';
import { useDrawingArea } from '@mui/x-charts/hooks';
import { styled } from '@mui/material/styles';
import "./Statistics.css";

// Styled text for the center label
const StyledText = styled('text')(({ theme }) => ({
  fill: theme.palette.text.primary,
  textAnchor: 'middle',
  dominantBaseline: 'central',
  fontWeight: 'bold',
}));

// Component for placing text in the center of the PieChart
function PieCenterLabel({ children }) {
  const { width, height, left, top } = useDrawingArea();
  return (
    <StyledText x={left + width / 2} y={top + height / 2}>
      {children}
    </StyledText>
  );
}

export default function Statistics({ title, values, colors }) {
  // Prepare the data based on values and colors props
  const data = values.map((value, index) => ({
    value,
    color: colors[index] || '#808080', // Default to gray if no color is provided for a slice
  }));
  const total = data.reduce((acc, curr) => acc + curr.value, 0);
  const percentage = total > 0 ? ((data[0].value / total) * 100).toFixed(1) : 0;
  return (
    <div className="stat-item">
      <PieChart
        series={[{
          data,
          innerRadius:75,
        }]}
        width={300}
        height={300}
      >
        <PieCenterLabel>{percentage}</PieCenterLabel>
      </PieChart>
      <div className='pie-title'>{title}</div>

    </div>
  );
}
