class Lease:
    def __init__(self, id, tenant_id, selected_space, minimum_required_space, total_volume, total_weight, term_months, status, start_date, end_date):
        self.id = id
        self.tenant_id = tenant_id
        self.selected_space = selected_space
        self.minimum_required_space = minimum_required_space
        self.total_volume = total_volume
        self.total_weight = total_weight
        self.term_months = term_months
        self.status = status
        self.start_date = start_date
        self.end_date = end_date

    # def calculate_minimum_required_space:
        

    # def create_lease(self, tenant_id, selected_space, minimum_required_space, total_volume, total_weight, term_months, start_date, end_date):
    #       minimum_space = total_volume
    #       if selected_space < minimum_required_space:
    #            raise ValueError("space less than minimum required space is not valid")
