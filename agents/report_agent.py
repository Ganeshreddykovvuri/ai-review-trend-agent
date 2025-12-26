class ReportAgent:
    def save(self, df, path):
        df.to_csv(path)
