"use client"
import { Select } from "@radix-ui/themes";
import { useEffect, useState } from 'react';
import { Lato } from "next/font/google";
const lato = Lato({weight: ["400"], subsets: ["latin"] });
import 'chartjs-adapter-date-fns';
import { startOfDay, format } from 'date-fns'; // Import date-fns functions
import { Chart as ChartJS, registerables } from 'chart.js';
import { Chart } from 'react-chartjs-2'
ChartJS.register(...registerables);

const fake_data = {
  "timeline": {
      "bloomberg": {
          "meta": [
              {
                  "score": 0.743,
                  "date": "Thu, 21 Mar 2024 07:00:00 GMT"
              }
          ],
          "apple": [
              {
                  "score": 0.0,
                  "date": "Mon, 18 Mar 2024 07:00:00 GMT"
              },
              {
                  "score": 0.5994,
                  "date": "Mon, 18 Mar 2024 07:00:00 GMT"
              },
              {
                  "score": 0.8519,
                  "date": "Sun, 24 Mar 2024 07:00:00 GMT"
              },
              {
                  "score": 0.4767,
                  "date": "Mon, 18 Mar 2024 18:09:48 GMT"
              },
              {
                  "score": 0.4404,
                  "date": "Sun, 17 Mar 2024 07:00:00 GMT"
              },
              {
                  "score": 0.4404,
                  "date": "Sun, 17 Mar 2024 07:00:00 GMT"
              },
              {
                  "score": 0.0,
                  "date": "Fri, 22 Mar 2024 07:00:00 GMT"
              },
              {
                  "score": 0.3612,
                  "date": "Sun, 10 Mar 2024 08:00:00 GMT"
              },
              {
                  "score": 0.3612,
                  "date": "Sun, 10 Mar 2024 08:00:00 GMT"
              },
              {
                  "score": 0.0,
                  "date": "Mon, 11 Mar 2024 07:00:00 GMT"
              },
              {
                  "score": -0.3818,
                  "date": "Wed, 03 Apr 2024 20:10:26 GMT"
              },
              {
                  "score": 0.0,
                  "date": "Wed, 27 Mar 2024 07:00:00 GMT"
              }
          ],
          "nvidia": [
              {
                  "score": 0.743,
                  "date": "Thu, 21 Mar 2024 07:00:00 GMT"
              },
              {
                  "score": 0.0,
                  "date": "Tue, 19 Mar 2024 07:00:00 GMT"
              },
              {
                  "score": 0.0,
                  "date": "Sun, 17 Mar 2024 07:00:00 GMT"
              },
              {
                  "score": 0.0,
                  "date": "Mon, 18 Mar 2024 07:00:00 GMT"
              },
              {
                  "score": 0.5994,
                  "date": "Mon, 18 Mar 2024 07:00:00 GMT"
              },
              {
                  "score": 0.1027,
                  "date": "Tue, 26 Mar 2024 07:00:00 GMT"
              },
              {
                  "score": 0.0,
                  "date": "Mon, 18 Mar 2024 07:00:00 GMT"
              }
          ],
          "google": [
              {
                  "score": 0.0,
                  "date": "Mon, 18 Mar 2024 07:00:00 GMT"
              },
              {
                  "score": 0.5106,
                  "date": "Fri, 05 Apr 2024 11:30:22 GMT"
              },
              {
                  "score": 0.4767,
                  "date": "Mon, 18 Mar 2024 18:09:48 GMT"
              }
          ],
          "amazon": [
              {
                  "score": 0.1779,
                  "date": "Wed, 27 Mar 2024 07:00:00 GMT"
              },
              {
                  "score": 0.1779,
                  "date": "Wed, 03 Apr 2024 16:10:29 GMT"
              }
          ]
      },
      "cnbc": {
          "meta": [
              {
                  "score": -0.7964,
                  "date": "Mon, 11 Mar 2024 07:00:00 GMT"
              }
          ],
          "apple": [
              {
                  "score": 0.4588,
                  "date": "Mon, 18 Mar 2024 07:00:00 GMT"
              },
              {
                  "score": 0.4019,
                  "date": "Fri, 22 Mar 2024 07:00:00 GMT"
              },
              {
                  "score": 0.0,
                  "date": "Tue, 26 Mar 2024 07:00:00 GMT"
              },
              {
                  "score": 0.0,
                  "date": "Tue, 12 Mar 2024 07:00:00 GMT"
              },
              {
                  "score": 0.0772,
                  "date": "Thu, 21 Mar 2024 07:00:00 GMT"
              }
          ],
          "nvidia": [
              {
                  "score": 0.34,
                  "date": "Mon, 18 Mar 2024 07:00:00 GMT"
              },
              {
                  "score": 0.3612,
                  "date": "Mon, 11 Mar 2024 07:00:00 GMT"
              },
              {
                  "score": -0.4215,
                  "date": "Tue, 19 Mar 2024 07:00:00 GMT"
              },
              {
                  "score": 0.0,
                  "date": "Tue, 19 Mar 2024 07:00:00 GMT"
              },
              {
                  "score": 0.0,
                  "date": "Fri, 08 Mar 2024 08:00:00 GMT"
              },
              {
                  "score": 0.0516,
                  "date": "Fri, 15 Mar 2024 07:00:00 GMT"
              },
              {
                  "score": 0.4767,
                  "date": "Thu, 14 Mar 2024 07:00:00 GMT"
              },
              {
                  "score": 0.0,
                  "date": "Fri, 05 Apr 2024 06:42:06 GMT"
              },
              {
                  "score": 0.0,
                  "date": "Thu, 04 Apr 2024 12:33:41 GMT"
              }
          ],
          "google": [],
          "amazon": [
              {
                  "score": 0.1779,
                  "date": "Wed, 27 Mar 2024 07:00:00 GMT"
              }
          ]
      }
  },
  "sentiments": {
      "meta": [
          0.743,
          -0.7964
      ],
      "apple": [
          0.26245,
          0.18758000000000002
      ],
      "nvidia": [
          0.20644285714285715,
          0.08977777777777779
      ],
      "google": [
          0.3291,
          0
      ],
      "amazon": [
          0.1779,
          0.1779
      ]
  }
}
export default function Home() {

  const [setRange, setTimeRange] = useState('1wk')
  const [selectedStrategy, setSelectedStrategy] = useState('active')
  const [selectedMarket, setSelectedMarket] = useState('tech')
  const [selectedCompany, setSelectedCompany] = useState('apple');
  const [selectedFeed, setSelectedFeed] = useState('bloomberg');
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: []
  });

  useEffect(() => {
    //@ts-ignore
    const companyData = fake_data['timeline'][selectedFeed][selectedCompany];
    //@ts-ignore
    const aggregatedData = companyData.reduce((acc, item) => {
      const dateKey = startOfDay(new Date(item.date)).toISOString();
      if (!acc[dateKey]) {
        acc[dateKey] = [];
      }
      acc[dateKey].push(item.score);
      return acc;
    }, {});

    const labels = Object.keys(aggregatedData).sort();
    const data = labels.map(date => {
      const scores = aggregatedData[date] || [];
      //@ts-ignore
      const averageScore = scores.reduce((sum, score) => sum + score, 0) / scores.length;
      return averageScore || 0;
    });

    setChartData({
      //@ts-ignore
      labels: labels.map(date => format(new Date(date), 'MM/dd/yyyy')),
      //@ts-ignore
      datasets: [{
        //@ts-ignore
        label: `${selectedFeed.toUpperCase()} - ${selectedCompany.toUpperCase()}`,
        data: data,
        borderWidth: 1
      }]
    });
  }, [selectedCompany, selectedFeed]);

  return (
    <main className="flex min-h-screen text-black flex-col items-center justify-between p-24">
      <div className="max-w-5xl w-full items-center flex-col justify-between font-mono text-sm lg:flex">
        <h1 className="text-4xl mb-10">Welcome Investor</h1>
        
        {/* Selectors for Strategy and Market (placeholder functionality) */}
        <div className="mb-10 flex flex-col">
          <h1 className="mb-11">What is your investment strategy?</h1>
          <Select.Root onValueChange={setSelectedStrategy}>
            <Select.Trigger>Strategy</Select.Trigger>
            <Select.Content>
              <Select.Item value="activist">Activist</Select.Item>
              <Select.Item value="growth">Growth</Select.Item>
            </Select.Content>
          </Select.Root>
        </div>
  
        <div className="mb-10 flex flex-col">
          <h1 className="mb-11">What market are you interested in investing in?</h1>
          <Select.Root onValueChange={setSelectedMarket} defaultValue="apple">
            <Select.Trigger>Choose Market</Select.Trigger>
            <Select.Content>
              <Select.Item value="tech">Tech</Select.Item>
              <Select.Item value="retail">Retail</Select.Item>
              <Select.Item value="transport">Transport</Select.Item>
            </Select.Content>
          </Select.Root>
        </div>
        <div className="mb-10 flex flex-col">
          <h1 className="mb-11">How far back to you want to go?</h1>
          <Select.Root onValueChange={setTimeRange} defaultValue="1wk">
            <Select.Trigger>Time Range</Select.Trigger>
            <Select.Content>
              <Select.Item value="1d">A day</Select.Item>
              <Select.Item value="1wk">A week</Select.Item>
              <Select.Item value="2wk">2 weeks</Select.Item>
              <Select.Item value="1m">1 month</Select.Item>
              <Select.Item value="5m">5 months</Select.Item>
            </Select.Content>
          </Select.Root>
        </div>
        
        {chartData && (
          <>
          <div className="flex flex-row w-full justify-evenly">
              <div className="mb-10 flex flex-col">
              <h1 className="mb-11">Company</h1>
              <Select.Root onValueChange={setSelectedFeed} defaultValue="bloomberg">
                <Select.Trigger>Select Feed</Select.Trigger>
                <Select.Content>
                  <Select.Item value="bloomberg">Bloomberg</Select.Item>
                  <Select.Item value="cnbc">CNBC</Select.Item>
                </Select.Content>
              </Select.Root>
              </div>
            <div className="mb-10 flex flex-col">
              <h1 className="mb-11">News Feed</h1>
              <Select.Root onValueChange={setSelectedCompany}>
                <Select.Trigger>{selectedCompany}</Select.Trigger>
                <Select.Content>
                  <Select.Item value="apple">Apple</Select.Item>
                  <Select.Item value="nvidia">Nvidia</Select.Item>
                  <Select.Item value="google">Google</Select.Item>
                  <Select.Item value="amazon">Amazon</Select.Item>
                </Select.Content>
              </Select.Root>
              </div>
          </div>
          <Chart
            type="line"
            data={chartData}
            options={{
              scales: {
                y: {
                  beginAtZero: false,
                  suggestedMin: -1,
                  suggestedMax: 1,
                  ticks: {
                    stepSize: 0.5
                  }
                }
              }
            }}
          />

          </>
        )}
      </div>
    </main>
  );
}
