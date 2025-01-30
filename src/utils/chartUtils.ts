export const roundDurationChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top' as const,
    },
  },
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: 'Duration (seconds)',
        color: 'white'
      }
    }
  }
}

export const createRoundDurationChartData = (rounds: { round_number: number; duration_seconds: number }[]) => ({
  labels: rounds.map(r => `Round ${r.round_number}`),
  datasets: [
    {
      label: '',
      data: rounds.map(r => r.duration_seconds),
      backgroundColor: '#4F46E5',
      borderColor: '#4338CA',
      borderWidth: 1,
      color: 'white'
    }
  ]
})