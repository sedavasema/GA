import random
from typing import List, Dict, Any
from ga.core import GA
from POPULATION import POPULATION

class SYSTEMMODEL:
    def __init__(self):
        self.pmNumber: int = 0
        self.vmNumber: int = 0
        self.replicationFactor: int = 4
        self.blockNumber: int = 0
        self.pmDefinition: List[Dict[str, Any]] = []
        self.vmTemplate: List[Dict[str, Any]] = []
        self.blockLoad: List[Dict[str, float]] = []
        self.customerProfiles: List[Dict[str, Any]] = []
        self.customerBudgets: List[int] = []
        self.customer_count: int = 0
        self.vm_per_customer: int = 0
        self.pmStatus: List[Dict[str, Any]] = []
        
        # ثابت‌های جدید
        self.ENERGY_PRICE = 0.1
        self.SLA_PENALTY_RATE = 500.0
        self.BUDGET_PENALTY_WEIGHT = 0.5
        self.FITNESS_SLA_MULTIPLIER = 10.0
        self.VM_COST_RATIO = 0.7
        
        # متغیرهای جدید برای ذخیره وضعیت منابع
        self.cached_pm_status = []  # ذخیره وضعیت PMها
        self.cached_vm_status = []  # ذخیره وضعیت VMها
        self.resource_status_initialized = False  # آیا وضعیت منابع مقداردهی اولیه شده؟

    def pm_generate(self, pm_count: int) -> None:
        pm_models = [
            {"model": "Dell R740", "cpu": 64, "io": 70, "net": 80, "energyIdle": 100, "energyMax": 300, "minfailrate": 0.002},
            {"model": "Dell R640", "cpu": 48, "io": 65, "net": 75, "energyIdle": 95, "energyMax": 280, "minfailrate": 0.003},
            {"model": "HPE DL380", "cpu": 56, "io": 60, "net": 70, "energyIdle": 90, "energyMax": 260, "minfailrate": 0.0025},
            {"model": "HPE DL360", "cpu": 40, "io": 55, "net": 65, "energyIdle": 85, "energyMax": 240, "minfailrate": 0.003},
            {"model": "Lenovo SR650", "cpu": 72, "io": 80, "net": 85, "energyIdle": 110, "energyMax": 310, "minfailrate": 0.0015},
            {"model": "Cisco C220", "cpu": 48, "io": 60, "net": 75, "energyIdle": 100, "energyMax": 290, "minfailrate": 0.002},
            {"model": "Fujitsu RX2540", "cpu": 64, "io": 70, "net": 80, "energyIdle": 95, "energyMax": 280, "minfailrate": 0.0022},
            {"model": "Supermicro 1029U", "cpu": 56, "io": 65, "net": 78, "energyIdle": 92, "energyMax": 275, "minfailrate": 0.002},
            {"model": "Huawei Pro", "cpu": 60, "io": 68, "net": 82, "energyIdle": 105, "energyMax": 295, "minfailrate": 0.0021},
            {"model": "Inspur NF5280", "cpu": 64, "io": 72, "net": 85, "energyIdle": 98, "energyMax": 300, "minfailrate": 0.0018},
            {"model": "Oracle X8-2L", "cpu": 48, "io": 66, "net": 76, "energyIdle": 97, "energyMax": 285, "minfailrate": 0.0024},
            {"model": "Tyan HX", "cpu": 52, "io": 62, "net": 73, "energyIdle": 96, "energyMax": 278, "minfailrate": 0.0023}
        ]
        
        self.pmNumber = pm_count
        self.pmDefinition = []
        self.pmStatus = []
        for i in range(pm_count):
            pm = random.choice(pm_models)
            self.pmDefinition.append(pm)
            self.pmStatus.append({'id': i, 'active': False, 'allocated_vms': []})

    def vm_generate(self, customer_count: int, vm_per_customer: int) -> None:
        self.customer_count = customer_count
        self.vm_per_customer = vm_per_customer
        self.vmNumber = customer_count * vm_per_customer
        self.vmTemplate = [
            {"type": "t3.micro", "cpu": 2, "io": 5, "net": 5, "cost": 5000},
            {"type": "t3.small", "cpu": 2, "io": 10, "net": 10, "cost": 7000},
            {"type": "t3.medium", "cpu": 2, "io": 15, "net": 15, "cost": 9000},
            {"type": "t3.large", "cpu": 2, "io": 20, "net": 20, "cost": 11000},
            {"type": "t3.xlarge", "cpu": 4, "io": 25, "net": 25, "cost": 15000},
            {"type": "m5.large", "cpu": 4, "io": 30, "net": 30, "cost": 20000},
            {"type": "m5.xlarge", "cpu": 8, "io": 35, "net": 35, "cost": 25000},
            {"type": "m5.2xlarge", "cpu": 8, "io": 40, "net": 40, "cost": 30000},
            {"type": "c5.large", "cpu": 4, "io": 28, "net": 30, "cost": 21000},
            {"type": "c5.xlarge", "cpu": 8, "io": 38, "net": 40, "cost": 27000},
            {"type": "c5.2xlarge", "cpu": 8, "io": 45, "net": 50, "cost": 35000},
            {"type": "r5.large", "cpu": 4, "io": 32, "net": 30, "cost": 22000},
            {"type": "r5.xlarge", "cpu": 8, "io": 40, "net": 35, "cost": 28000},
            {"type": "r5.2xlarge", "cpu": 8, "io": 50, "net": 50, "cost": 37000},
            {"type": "n2-standard-2", "cpu": 8, "io": 40, "net": 40, "cost": 34000},
            {"type": "n2-standard-4", "cpu": 16, "io": 60, "net": 60, "cost": 50000},
            {"type": "e2-standard-2", "cpu": 4, "io": 20, "net": 20, "cost": 12000},
            {"type": "e2-standard-4", "cpu": 8, "io": 40, "net": 40, "cost": 25000},
            {"type": "Standard_D2s_v3", "cpu": 2, "io": 20, "net": 25, "cost": 15000},
            {"type": "Standard_D4s_v3", "cpu": 4, "io": 40, "net": 40, "cost": 28000},
            {"type": "Standard_F2s_v2", "cpu": 2, "io": 25, "net": 30, "cost": 16000},
            {"type": "Standard_F4s_v2", "cpu": 4, "io": 35, "net": 45, "cost": 24000},
            {"type": "Standard_E2s_v3", "cpu": 2, "io": 30, "net": 30, "cost": 17000},
            {"type": "Standard_E4s_v3", "cpu": 4, "io": 40, "net": 50, "cost": 26000},
            {"type": "a2-highgpu-1g", "cpu": 12, "io": 50, "net": 60, "cost": 80000},
        ]

        self.customerProfiles = []
        self.customerBudgets = []
        for _ in range(customer_count):
            profile_type = random.choice(["economic", "standard", "enterprise"])
            blocks = random.choice([100, 250, 500])
            self.customerProfiles.append({"type": profile_type, "blocks": blocks})
            budget_ranges = {
                "economic": (5_000_000, 10_000_000),
                "standard": (10_000_000, 15_000_000),
                "enterprise": (15_000_000, 25_000_000),
            }
            min_b, max_b = budget_ranges[profile_type]
            self.customerBudgets.append(random.randint(min_b, max_b))

    def tpds_model(self, vm_number: int, file_num: int = 500) -> None:
        self.blockNumber = file_num
        self.blockLoad = []
        for _ in range(file_num * self.replicationFactor):
            self.blockLoad.append({
                "cpu": round(random.uniform(0.5, 1.5), 2),
                "io": round(random.uniform(0.5, 1.5), 2),
                "net": round(random.uniform(0.5, 1.5), 2),
            })
        print(f"Initialized {file_num} blocks with {file_num * self.replicationFactor} replications")

    def add_customer(self, profile_type: str, blocks: int, budget: int, vm_count: int = 2):
        self.customerProfiles.append({"type": profile_type, "blocks": blocks})
        self.customerBudgets.append(budget)
        self.customer_count += 1
        self.vmNumber += vm_count
        population_seed = 100 + self.customer_count
        evolution_seed = 200 + self.customer_count
        population = POPULATION(64)
        ga = GA(self, population_seed, evolution_seed, customer_num=self.customer_count - 1)
        ga.generate_population(population, self.customerBudgets)
        for gen in range(30):
            population = ga.evolve_nsga2(population, self.customerBudgets, gen, 30)
        print(f"مشتری جدید اضافه شد: پروفایل {profile_type}, بودجه {budget} تومان. تخصیص منابع به‌روزرسانی شد.")
        
        newly_activated = None
        active_pms = sum(1 for p in self.pmStatus if p['active'])
        if active_pms / self.pmNumber < 0.8:
            for p in self.pmStatus:
                if not p['active']:
                    p['active'] = True
                    newly_activated = p['id']
                    break
        if newly_activated is not None:
            print(f"PM {newly_activated} روشن شد برای مشتری جدید.")
        else:
            print("هیچ PM جدیدی روشن نشد. همه PMهای فعال کافی بودند.")
        print("مصرف انرژی فعلی: محاسبه‌شده. سود به‌روزرسانی شد.")
        
        # بازنشانی کش وضعیت منابع (برای به‌روزرسانی نمایش)
        self.resource_status_initialized = False
        self.initialize_resource_status()  # مقداردهی مجدد وضعیت منابع
        
    def initialize_resource_status(self):
        """مقداردهی اولیه وضعیت منابع (فقط یک بار اجرا می‌شود)"""
        import random
        
        self.cached_pm_status = []
        self.cached_vm_status = []
        
        # وضعیت PMها - فعال کردن نیمی از PMها
        for i, pm in enumerate(self.pmDefinition):
            if i < len(self.pmDefinition) // 2:  # نیمی از PMها فعال
                active = True
                allocated_vms = []  # ابتدا خالی میذاریم
            else:
                active = False
                allocated_vms = []
            
            if active:
                # محاسبه مصرف برق و منابع (ثابت و تصادفی فقط یک بار)
                idle_power = pm['energyIdle']
                max_power = pm['energyMax']
                power_usage = idle_power + (max_power - idle_power) * 0.3  # مصرف متوسط
                
                cpu_load = random.randint(40, 80)  # لود واقعی‌تر
                mem_load = random.randint(30, 70)
                io_load = random.randint(20, 60)
                net_load = random.randint(10, 50)
                
                pm_info = {
                    'id': i,
                    'model': pm['model'],
                    'status': 'روشن',
                    'power_usage': round(power_usage, 2),
                    'cpu_load': cpu_load,
                    'mem_load': mem_load,
                    'io_load': io_load,
                    'net_load': net_load,
                    'allocated_vms': allocated_vms
                }
            else:
                pm_info = {
                    'id': i,
                    'model': pm['model'],
                    'status': 'خاموش',
                    'power_usage': 0,
                    'cpu_load': 0,
                    'mem_load': 0,
                    'io_load': 0,
                    'net_load': 0,
                    'allocated_vms': []
                }
            self.cached_pm_status.append(pm_info)
        
        # وضعیت VMها - ایجاد یک VM برای هر مشتری
        vm_dict = {}
        active_pms = [pm for pm in self.cached_pm_status if pm['status'] == 'روشن']
        
        for customer_idx in range(len(self.customerProfiles)):
            # انتخاب یک PM فعال به صورت تصادفی
            if active_pms:
                pm = random.choice(active_pms)
                pm_id = pm['id']
                # اضافه کردن VM به لیست allocated_vms این PM
                vm_id = f"VM-{pm_id}-{len(pm['allocated_vms'])+1}"
                pm['allocated_vms'].append(vm_id)
            else:
                # اگر هیچ PM فعلی نبود، از PM صفر استفاده کن
                pm_id = 0
                vm_id = f"VM-{pm_id}-{customer_idx+1}"
            
            # اطلاعات مشتری
            profile = self.customerProfiles[customer_idx]
            budget = self.customerBudgets[customer_idx]
            
            # انتخاب یک نوع VM تصادفی
            vm_idx = random.randint(0, len(self.vmTemplate)-1)
            vm_type = self.vmTemplate[vm_idx]['type']
            vm_cost = self.vmTemplate[vm_idx]['cost']
            
            vm_dict[vm_id] = {
                'id': vm_id,
                'customer_idx': customer_idx,
                'customer_name': f"مشتری {customer_idx+1:02d}",  # فرمت دو رقمی
                'profile': profile['type'],
                'budget': budget,
                'blocks': profile['blocks'],
                'vm_type': vm_type,
                'vm_cost': vm_cost,
                'host_pm': pm_id
            }
        
        self.cached_vm_status = list(vm_dict.values())
        self.resource_status_initialized = True
        
        print(f"✅ وضعیت منابع مقداردهی اولیه شد: {len(self.cached_pm_status)} PM, {len(self.cached_vm_status)} VM")
    
    def get_realtime_status(self):
        """برگرداندن وضعیت ذخیره شده منابع (بدون تغییر در هر فراخوانی)"""
        if not self.resource_status_initialized:
            self.initialize_resource_status()
        
        return self.cached_pm_status, self.cached_vm_status