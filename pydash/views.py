# The MIT License (MIT)
#
# Copyright (c) 2014 Florian Neagu - michaelneagu@gmail.com - https://github.com/k3oni/
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse
from django.template import RequestContext

from settings import (TIME_JS_REFRESH, TIME_JS_REFRESH_LONG,
                      TIME_JS_REFRESH_NET, _VERSION)
import services
import urls


def get_pydash_urls():
    results = dict()
    for url_pattern in urls.urlpatterns:
        name = url_pattern.name
        try:
        # Works for non regex patterns
            results[name] = reverse(name)
        except Exception:
        # Get relative url prefix of regex patterns

        # Hacky solution but it works.
        # E.g. reverse('platform', args=[0])[:-2] -> /info/platform/
        #      reverse('getcpus', args[0])[:-2] -> /info/getcpus/
            results[name] = reverse(name, args=[0])[:-2]
    return json.dumps(results)


@login_required(login_url=reverse_lazy('login'))
def index(request):
    """

    Index page.

    """
    pydash_urls = get_pydash_urls()
    return render_to_response('main.html', {'time_refresh': TIME_JS_REFRESH,
                                            'time_refresh_long': TIME_JS_REFRESH_LONG,
                                            'time_refresh_net': TIME_JS_REFRESH_NET,
                                            'version': _VERSION,
                                            'pydashUrls': pydash_urls},
                              context_instance=RequestContext(request))


@login_required(login_url=reverse_lazy('login'))
def getnetstat(request):
    """
    Return netstat output
    """
    try:
        net_stat = services.get_netstat()
    except Exception:
        net_stat = None

    data = json.dumps(net_stat)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response


@login_required(login_url=reverse_lazy('login'))
def platform(request, name):
    """
    Return the hostname
    """
    getplatform = services.get_platform()
    hostname = getplatform['hostname']
    osname = getplatform['osname']
    kernel = getplatform['kernel']

    data = {}

    if name == 'hostname':
        try:
            data = hostname
        except Exception:
            data = None

    if name == 'osname':
        try:
            data = osname
        except Exception:
            data = None

    if name == 'kernel':
        try:
            data = kernel
        except Exception:
            data = None

    data = json.dumps(data)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response


@login_required(login_url=reverse_lazy('login'))
def getcpus(request, name):
    """
    Return the CPU number and type/model
    """
    cpus = services.get_cpus()
    cputype = cpus['type']
    cpucount = cpus['cpus']
    data = {}

    if name == 'type':
        try:
            data = cputype
        except Exception:
            data = None

    if name == 'count':
        try:
            data = cpucount
        except Exception:
            data = None

    data = json.dumps(data)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response


@login_required(login_url=reverse_lazy('login'))
def uptime(request):
    """
    Return uptime
    """
    try:
        up_time = services.get_uptime()
    except Exception:
        up_time = None

    data = json.dumps(up_time)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response


@login_required(login_url=reverse_lazy('login'))
def getdisk(request):
    """
    Return the disk usage
    """
    try:
        diskusage = services.get_disk()
    except Exception:
        diskusage = None

    data = json.dumps(diskusage)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response


@login_required(login_url=reverse_lazy('login'))
def getips(request):
    """
    Return the IPs and interfaces
    """
    try:
        get_ips = services.get_ipaddress()
    except Exception:
        get_ips = None

    data = json.dumps(get_ips['itfip'])
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response


@login_required(login_url=reverse_lazy('login'))
def getusers(request):
    """
    Return online users
    """
    try:
        online_users = services.get_users()
    except Exception:
        online_users = None

    data = json.dumps(online_users)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response


@login_required(login_url=reverse_lazy('login'))
def getproc(request):
    """
    Return the running processes
    """
    try:
        processes = services.get_cpu_usage()
        processes = processes['all']
    except Exception:
        processes = None

    data = json.dumps(processes)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response


@login_required(login_url=reverse_lazy('login'))
def cpuusage(request):
    """
    Return CPU Usage in %
    """
    try:
        cpu_usage = services.get_cpu_usage()

    except Exception:
        cpu_usage = 0

    cpu = [
        {
            "value": cpu_usage['free'],
            "color": "#0AD11B"
        },
        {
            "value": cpu_usage['used'],
            "color": "#F7464A"
        }
    ]

    data = json.dumps(cpu)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response


@login_required(login_url=reverse_lazy('login'))
def memusage(request):
    """
    Return Memory Usage in % and numeric
    """
    datasets_free = []
    datasets_used = []
    datasets_buffers = []
    datasets_cached = []

    try:
        mem_usage = services.get_mem()
    except Exception:
        mem_usage = 0

    try:
        cookies = request.COOKIES['memory_usage']
    except Exception:
        cookies = None

    if not cookies:
        datasets_free.append(0)
        datasets_used.append(0)
        datasets_buffers.append(0)
        datasets_cached.append(0)
    else:
        datasets = json.loads(cookies)
        datasets_free = datasets[0]
        datasets_used = datasets[1]
        atasets_buffers = datasets[2]
        datasets_cached = datasets[3]

    if len(datasets_free) > 10:
        while datasets_free:
            del datasets_free[0]
            if len(datasets_free) == 10:
                break
    if len(datasets_used) > 10:
        while datasets_used:
            del datasets_used[0]
            if len(datasets_used) == 10:
                break
    if len(datasets_buffers) > 10:
        while datasets_buffers:
            del datasets_buffers[0]
            if len(datasets_buffers) == 10:
                break
    if len(datasets_cached) > 10:
        while datasets_cached:
            del datasets_cached[0]
            if len(datasets_cached) == 10:
                break
    if len(datasets_free) <= 9:
        datasets_free.append(int(mem_usage['free']))
    if len(datasets_free) == 10:
        datasets_free.append(int(mem_usage['free']))
        del datasets_free[0]
    if len(datasets_used) <= 9:
        datasets_used.append(int(mem_usage['usage']))
    if len(datasets_used) == 10:
        datasets_used.append(int(mem_usage['usage']))
        del datasets_used[0]
    if len(datasets_buffers) <= 9:
        datasets_buffers.append(int(mem_usage['buffers']))
    if len(datasets_buffers) == 10:
        datasets_buffers.append(int(mem_usage['buffers']))
        del datasets_buffers[0]
    if len(datasets_cached) <= 9:
        datasets_cached.append(int(mem_usage['cached']))
    if len(datasets_cached) == 10:
        datasets_cached.append(int(mem_usage['cached']))
        del datasets_cached[0]
    # Some fix division by 0 Chart.js
    if len(datasets_free) == 10:
        if sum(datasets_free) == 0:
            datasets_free[9] += 0.1
        if sum(datasets_free) / 10 == datasets_free[0]:
            datasets_free[9] += 0.1

    memory = {
        'labels': [""] * 10,
        'datasets': [
            {
                "fillColor": "rgba(247,70,74,0.5)",
                "strokeColor": "rgba(247,70,74,1)",
                "pointColor": "rgba(247,70,74,1)",
                "pointStrokeColor": "#fff",
                "data": datasets_used
            },
            {
                "fillColor": "rgba(43,214,66,0.5)",
                "strokeColor": "rgba(43,214,66,1)",
                "pointColor": "rgba(43,214,66,1)",
                "pointStrokeColor": "#fff",
                "data": datasets_free
            },
            {
                "fillColor": "rgba(0,154,205,0.5)",
                "strokeColor": "rgba(0,154,205,1)",
                "pointColor": "rgba(0,154,205,1)",
                "pointStrokeColor": "#fff",
                "data": datasets_buffers
            },
            {
                "fillColor": "rgba(255,185,15,0.5)",
                "strokeColor": "rgba(255,185,15,1)",
                "pointColor": "rgba(265,185,15,1)",
                "pointStrokeColor": "#fff",
                "data": datasets_cached
            } 
        ]
    }

    cookie_memory = [datasets_free, datasets_used, datasets_buffers, datasets_cached]
    data = json.dumps(memory)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.cookies['memory_usage'] = cookie_memory
    response.write(data)
    return response


@login_required(login_url=reverse_lazy('login'))
def loadaverage(request):
    """
    Return Load Average numeric
    """
    datasets = []

    try:
        load_average = services.get_load()
    except Exception:
        load_average = 0

    try:
        cookies = request.COOKIES['load_average']
    except Exception:
        cookies = None

    if not cookies:
        datasets.append(0)
    else:
        datasets = json.loads(cookies)
    if len(datasets) > 10:
        while datasets:
            del datasets[0]
            if len(datasets) == 10:
                break
    if len(datasets) <= 9:
        datasets.append(float(load_average))
    if len(datasets) == 10:
        datasets.append(float(load_average))
        del datasets[0]

    # Some fix division by 0 Chart.js
    if len(datasets) == 10:
        if sum(datasets) == 0:
            datasets[9] += 0.1
        if sum(datasets) / 10 == datasets[0]:
            datasets[9] += 0.1

    load = {
        'labels': [""] * 10,
        'datasets': [
            {
                "fillColor": "rgba(151,187,205,0.5)",
                "strokeColor": "rgba(151,187,205,1)",
                "pointColor": "rgba(151,187,205,1)",
                "pointStrokeColor": "#fff",
                "data": datasets
            }
        ]
    }

    data = json.dumps(load)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.cookies['load_average'] = datasets
    response.write(data)
    return response


@login_required(login_url=reverse_lazy('login'))
def gettraffic(request):
    """
    Return the traffic for the interface
    """
    datasets_in = []
    datasets_in_i = []
    datasets_out = []
    datasets_out_o = []
    label = "KBps"

    try:
        intf = services.get_ipaddress()
        intf = intf['interface'][0]

        traffic = services.get_traffic(intf)
    except Exception:
        traffic = 0

    try:
        cookies = request.COOKIES['traffic']
    except Exception:
        cookies = None

    if not cookies:
        datasets_in.append(0)
        datasets_in_i.append(0)
        datasets_out.append(0)
        datasets_out_o.append(0)
    else:
        datasets = json.loads(cookies)
        datasets_in = datasets[0]
        datasets_out = datasets[1]
        datasets_in_i = datasets[2]
        datasets_out_o = datasets[3]

    if len(datasets_in) > 10:
        while datasets_in:
            del datasets_in[0]
            if len(datasets_in) == 10:
                break
    if len(datasets_in_i) > 2:
        while datasets_in_i:
            del datasets_in_i[0]
            if len(datasets_in_i) == 2:
                break
    if len(datasets_out) > 10:
        while datasets_out:
            del datasets_out[0]
            if len(datasets_out) == 10:
                break
    if len(datasets_out_o) > 2:
        while datasets_out_o:
            del datasets_out_o[0]
            if len(datasets_out_o) == 2:
                break

    if len(datasets_in_i) <= 1:
        datasets_in_i.append(float(traffic['traffic_in']))
    if len(datasets_in_i) == 2:
        datasets_in_i.append(float(traffic['traffic_in']))
        del datasets_in_i[0]
    if len(datasets_out_o) <= 1:
        datasets_out_o.append(float(traffic['traffic_out']))
    if len(datasets_out_o) == 2:
        datasets_out_o.append(float(traffic['traffic_out']))
        del datasets_out_o[0]

    dataset_in = (
        float(((datasets_in_i[1] - datasets_in_i[0]) / 1024) / (TIME_JS_REFRESH_NET / 1000)))
    dataset_out = (
        float(((datasets_out_o[1] - datasets_out_o[0]) / 1024) / (TIME_JS_REFRESH_NET / 1000)))

    if dataset_in > 1024 or dataset_out > 1024:
        dataset_in = (float(dataset_in / 1024))
        dataset_out = (float(dataset_out / 1024))
        label = "MBps"

    if len(datasets_in) <= 9:
        datasets_in.append(dataset_in)
    if len(datasets_in) == 10:
        datasets_in.append(dataset_in)
        del datasets_in[0]
    if len(datasets_out) <= 9:
        datasets_out.append(dataset_out)
    if len(datasets_out) == 10:
        datasets_out.append(dataset_out)
        del datasets_out[0]

    # Some fix division by 0 Chart.js
    if len(datasets_in) == 10:
        if sum(datasets_in) == 0:
            datasets_in[9] += 0.1
        if sum(datasets_in) / 10 == datasets_in[0]:
            datasets_in[9] += 0.1

    traff = {
        'labels': [label] * 10,
        'datasets': [
            {
                "fillColor": "rgba(105,210,231,0.5)",
                "strokeColor": "rgba(105,210,231,1)",
                "pointColor": "rgba(105,210,231,1)",
                "pointStrokeColor": "#fff",
                "data": datasets_in
            },
            {
                "fillColor": "rgba(227,48,81,0.5)",
                "strokeColor": "rgba(227,48,81,1)",
                "pointColor": "rgba(227,48,81,1)",
                "pointStrokeColor": "#fff",
                "data": datasets_out
            }
        ]
    }

    cookie_traffic = [datasets_in, datasets_out, datasets_in_i, datasets_out_o]
    data = json.dumps(traff)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.cookies['traffic'] = cookie_traffic
    response.write(data)
    return response


@login_required(login_url=reverse_lazy('login'))
def getdiskio(request):
    """
    Return the reads and writes for the drive
    """
    datasets_in = []
    datasets_in_i = []
    datasets_out = []
    datasets_out_o = []

    try:
        diskrw = services.get_disk_rw()
        diskrw = diskrw[0]
    except Exception:
        diskrw = 0

    try:
        cookies = request.COOKIES['diskrw']
    except Exception:
        cookies = None

    if not cookies:
        datasets_in.append(0)
        datasets_in_i.append(0)
        datasets_out.append(0)
        datasets_out_o.append(0)
    else:
        datasets = json.loads(cookies)
        datasets_in = datasets[0]
        datasets_out = datasets[1]
        datasets_in_i = datasets[2]
        datasets_out_o = datasets[3]

    if len(datasets_in) > 10:
        while datasets_in:
            del datasets_in[0]
            if len(datasets_in) == 10:
                break
    if len(datasets_in_i) > 2:
        while datasets_in_i:
            del datasets_in_i[0]
            if len(datasets_in_i) == 2:
                break
    if len(datasets_out) > 10:
        while datasets_out:
            del datasets_out[0]
            if len(datasets_out) == 10:
                break
    if len(datasets_out_o) > 2:
        while datasets_out_o:
            del datasets_out_o[0]
            if len(datasets_out_o) == 2:
                break

    if len(datasets_in_i) <= 1:
        datasets_in_i.append(int(diskrw[1]))
    if len(datasets_in_i) == 2:
        datasets_in_i.append(int(diskrw[1]))
        del datasets_in_i[0]
    if len(datasets_out_o) <= 1:
        datasets_out_o.append(int(diskrw[2]))
    if len(datasets_out_o) == 2:
        datasets_out_o.append(int(diskrw[2]))
        del datasets_out_o[0]

    dataset_in = (
        int((datasets_in_i[1] - datasets_in_i[0]) / (TIME_JS_REFRESH_NET / 1000)))
    dataset_out = (
        int((datasets_out_o[1] - datasets_out_o[0]) / (TIME_JS_REFRESH_NET / 1000)))

    if len(datasets_in) <= 9:
        datasets_in.append(dataset_in)
    if len(datasets_in) == 10:
        datasets_in.append(dataset_in)
        del datasets_in[0]
    if len(datasets_out) <= 9:
        datasets_out.append(dataset_out)
    if len(datasets_out) == 10:
        datasets_out.append(dataset_out)
        del datasets_out[0]

    # Some fix division by 0 Chart.js
    if len(datasets_in) == 10:
        if sum(datasets_in) == 0:
            datasets_in[9] += 0.1
        if sum(datasets_in) / 10 == datasets_in[0]:
            datasets_in[9] += 0.1

    disk_rw = {
        'labels': [""] * 10,
        'datasets': [
            {
                "fillColor": "rgba(245,134,15,0.5)",
                "strokeColor": "rgba(245,134,15,1)",
                "pointColor": "rgba(245,134,15,1)",
                "pointStrokeColor": "#fff",
                "data": datasets_in
            },
            {
                "fillColor": "rgba(15,103,245,0.5)",
                "strokeColor": "rgba(15,103,245,1)",
                "pointColor": "rgba(15,103,245,1)",
                "pointStrokeColor": "#fff",
                "data": datasets_out
            }
        ]
    }

    cookie_diskrw = [datasets_in, datasets_out, datasets_in_i, datasets_out_o]
    data = json.dumps(disk_rw)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.cookies['diskrw'] = cookie_diskrw
    response.write(data)
    return response
